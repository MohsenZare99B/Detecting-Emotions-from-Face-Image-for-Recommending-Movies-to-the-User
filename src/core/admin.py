from django.contrib import admin
from .models import Movie, Users, Movie_feature, Vote, Emotional_state_feature, Comment
from .models import Romance_pic, Horror_pic, Comedy_pic, Action_pic, Fantasy_pic
# Register your models here.
admin.site.register(Movie)
admin.site.register(Users)
admin.site.register(Vote)
admin.site.register(Movie_feature)
admin.site.register(Emotional_state_feature)

admin.site.register(Romance_pic)
admin.site.register(Horror_pic)
admin.site.register(Comedy_pic)
admin.site.register(Action_pic)
admin.site.register(Fantasy_pic)
admin.site.register(Comment)
