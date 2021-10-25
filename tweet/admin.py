from django.contrib import admin
from tweet.models import *
# Register your models here.
admin.site.register(Tweets)
admin.site.register(TweetMedia)