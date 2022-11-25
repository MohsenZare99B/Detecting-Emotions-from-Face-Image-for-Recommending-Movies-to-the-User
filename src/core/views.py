from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Movie, Users, Vote, Movie_feature, Emotional_state_feature, Comment
from .models import Action_pic, Horror_pic, Comedy_pic, Fantasy_pic, Romance_pic
import random
from pathlib import Path
from keras.models import load_model
import cv2
import numpy as np
from PIL import Image

def movie(request, pk):
    movie_item = Movie.objects.get(id=pk)
    context = {"movie": movie_item}
    if request.method == 'POST':
        romance = request.POST.get('romance')
        horror = request.POST.get('horror')
        comedy = request.POST.get('comedy')
        action = request.POST.get('action')
        fantasy = request.POST.get('fantasy')
        Vote.objects.create(movie=movie_item, romance=romance, horror=horror,
                    comedy=comedy, action=action, fantasy=fantasy, username=request.session["user"])
        try:
            feature_item = Movie_feature.objects.get(movie=movie_item)
            Movie_feature.objects.create(movie=movie_item, 
            romance=int(romance) + feature_item.romance,
            horror=int(horror) + feature_item.horror, comedy=int(comedy) + feature_item.comedy,
             action=int(action) + feature_item.action, fantasy=int(fantasy) + feature_item.fantasy,
             no_of_votes=1 + feature_item.no_of_votes)
            feature_item.delete()
        except Movie_feature.DoesNotExist:
            Movie_feature.objects.create(movie=movie_item, romance=romance,
            horror=horror, comedy=comedy, action=action, fantasy=fantasy,
             no_of_votes=1)

    if "user" not in request.session:
        context['vote_message'] = "You must login to vote..."
    else:
        try:
            vote = Vote.objects.get(movie=movie_item, username=request.session['user'])
            context['vote_message'] = "You have already voted for this movie"
        except Vote.DoesNotExist:
            context['vote_message'] = "You can vote..."
            context['can_vote'] = True
    try:
        feature_item = Movie_feature.objects.get(movie=movie_item)
        T = feature_item.no_of_votes
        context["votes"]= T
        context["romance"]= "width:"+ str(10 * feature_item.romance / T) +"%"
        context["horror"]= "width:"+ str(10 * feature_item.horror / T) +"%"
        context["comedy"]= "width:"+ str(10 * feature_item.comedy / T) +"%"
        context["action"]= "width:"+ str(10 * feature_item.action / T) +"%"
        context["fantasy"]= "width:"+ str(10 * feature_item.fantasy / T) +"%"
    except Movie_feature.DoesNotExist:
        context["votes"]= 0
        context["romance"]= "width:"+ str(50) +"%"
        context["horror"]= "width:"+ str(50) +"%"
        context["comedy"]= "width:"+ str(50) +"%"
        context["action"]= "width:"+ str(50) +"%"
        context["fantasy"]= "width:"+ str(50) +"%"
    comments = Comment.objects.filter(movie=movie_item)
    context["comments"] = comments
    return render(request, 'core/movie.html', context)

def movies(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    movies = Movie.objects.filter(title__icontains=search_query)
    page = request.GET.get('page')

    results = 6
    paginator = Paginator(movies, results)
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        movies = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        movies = paginator.page(page)
    context = {"movies": movies, "search_query": search_query,
                "paginator": paginator}
    if "message" in request.session:
        context["message"] = request.session["message"]
        del request.session["message"]
    return render(request, 'core/movies.html', context)

def login_user(request):
    context= {"login":True, "register": False}
    if "user" in request.session:
        return redirect("index")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = Users.objects.get(username=username, password=password)
        except Users.DoesNotExist:
            user = None

        if user:
            request.session["user"] = username
            request.session["message"] = "Logged in successfully!"
            return redirect("index")           
        else:
            context["message"] = "Username or Password is incorrect!"
    return render(request, 'core/login_register.html', context)

def logout_user(request):
    if "user" in request.session:
        del request.session["user"]
    return redirect("index")

def register_user(request):
        context= {"login":False, "register": True}
        if "user" in request.session:
            return redirect("index")
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = Users.objects.get(username=username)
            except Users.DoesNotExist:
                user = None
            if user:
                context["message"] = "User Already Exists"
            else:
                user = Users.objects.create(username=username, password=password)
                request.session["user"] = username
                request.session["message"] = "Account created successfully!"
                return redirect("index")
        return render(request, 'core/login_register.html', context)

def index(request):
    return redirect("movies")

def result(request):
    context = {}
    fer = request.session["fer"]
    for i in range(len(fer)):
        fer[i] *= 100
        fer[i] = int(round(fer[i]))
        fer[i] = min(fer[i], 100)
    context["angry"]= "width:"+ str(fer[0]) +"%"
    context["disgust"]= "width:"+ str(fer[1]) +"%"
    context["fear"]= "width:"+ str(fer[2]) +"%"
    context["happy"]= "width:"+ str(fer[3]) +"%"
    context["neutral"]= "width:"+ str(fer[4]) +"%"
    context["sad"]= "width:"+ str(fer[5]) +"%"
    context["surprise"]= "width:"+ str(fer[6]) +"%"

    rec_movies = request.session['rec_movies']
    context["movie1"] = Movie.objects.get(id=rec_movies[0])
    context["movie2"] = Movie.objects.get(id=rec_movies[1])
    context["movie3"] = Movie.objects.get(id=rec_movies[2])
    return render(request, 'core/result.html', context)

def get_recommended_movies(emotional_state):
    movie_feature = []
    mfs = list(Movie_feature.objects.all())
    movie_objects = []
    for mf in mfs:
        no = mf.no_of_votes
        movie_feature.append([mf.romance / no, mf.horror / no, mf.comedy / no, mf.action / no, mf.fantasy / no])
        movie_objects.append(str(mf.movie.id))
    movie_feature = np.array(movie_feature)
    feature_movie = movie_feature.T
    esf = Emotional_state_feature.objects.get(emotional_state=emotional_state)
    no_esf = esf.no_of_votes
    emotional_state_feature = [esf.romance / no_esf, esf.horror / no_esf,
     esf.comedy / no_esf, esf.action / no_esf, esf.fantasy / no_esf]
    emotional_state_feature = np.array(emotional_state_feature)
    result = emotional_state_feature @ feature_movie
    top3 = result.argsort()[-3:][::-1]
    return [movie_objects[top3[0]], movie_objects[top3[1]], movie_objects[top3[2]]]

def fer(img):
    BASE_DIR = Path(__file__).resolve().parent.parent
    BASE_DIR = BASE_DIR / "image_processing"
    MODEL_PATH = BASE_DIR / "my_model.h5"
    XML_PATH = BASE_DIR / "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(str(XML_PATH))
    model = load_model(str(MODEL_PATH))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if type(faces) == type((1, 2)):
        return None
    (y, x, w, h) = faces[0]
    img = img[x:x+w, y:y+h].copy()
    img = cv2.resize(img, (48, 48))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = np.expand_dims(img, axis=0)
    return model.predict(img)

def get_emotional_state(x):
    ret = ""
    for i in range(len(x)):
        ret = ret + str(min(5, int(round(x[i] * 5))))
    return ret

def user_upload(request):
    if request.method == 'POST':
        image = request.FILES['file']
        image = Image.open(image)
        image = np.asarray(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        FER = fer(image)[0].tolist()
        request.session['fer'] = FER
        emotional_state = get_emotional_state(FER)
        Q = [-1 for i in range(5)]
        Q[int(request.POST['Radios'])] = 10
        try:
            e = Emotional_state_feature.objects.get(emotional_state=emotional_state)
            Emotional_state_feature.objects.create(
                emotional_state=emotional_state,
                romance=Q[0] + e.romance,
                horror=Q[1] + e.horror,
                comedy=Q[2] + e.comedy,
                action=Q[3] + e.action,
                fantasy=Q[4] + e.fantasy,
                no_of_votes=1 + e.no_of_votes
            )
            e.delete()
        except Emotional_state_feature.DoesNotExist:
            Emotional_state_feature.objects.create(
                emotional_state=emotional_state,
                romance=Q[0],
                horror=Q[1],
                comedy=Q[2],
                action=Q[3],
                fantasy=Q[4],
                no_of_votes=1
            )
        request.session["rec_movies"] = get_recommended_movies(emotional_state)
        return redirect('result')

    romantic_photos = list(Romance_pic.objects.all())
    romantic_photo = random.choice(romantic_photos)
    horror_photos = list(Horror_pic.objects.all())
    horror_photo = random.choice(horror_photos)
    comedy_photos = list(Comedy_pic.objects.all())
    comedy_photo = random.choice(comedy_photos)
    action_photos = list(Action_pic.objects.all())
    action_photo = random.choice(action_photos)
    fantasy_photos = list(Fantasy_pic.objects.all())
    fantasy_photo = random.choice(fantasy_photos)
    context = {"action_photo": action_photo, "fantasy_photo": fantasy_photo,
                "comedy_photo": comedy_photo, "horror_photo": horror_photo,
                "romantic_photo": romantic_photo}
    return render(request, "core/user_upload.html", context)

def comment(request, pk):
    if "user" not in request.session:
        return redirect("login")
    movie_item = Movie.objects.get(id=pk)
    context = {"movie": movie_item}
    if request.method == 'POST':
        comment_text = request.POST.get("comment")
        Comment.objects.create(movie=movie_item,
                                text=comment_text,
                                username=request.session['user'])
        return redirect('movie', pk=movie_item.id)
    return render(request, 'core/comment.html', context)