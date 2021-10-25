from rest_framework import serializers
from tweet.models import TweetMedia, Tweets

class TweetMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetMedia
        fields = '__all__'

class  TweetSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user_username')
    media_content = TweetMediaSerializer(many=True,  read_only=True)

    def get_user_username(self, tweets):
        user = tweets.user.username
        return user

    class Meta:
        model = Tweets
        fields = ['id','content', 'media_content', 'user']
        depth = 1


