from django.contrib import admin
from .models import Post
from .models import covid_tweet_data

admin.site.register(Post)
admin.site.register(covid_tweet_data)