from django.urls import path

from tweet.views import TweetAPIView
urlpatterns = [
    path('api/tweet', TweetAPIView.as_view()),
]