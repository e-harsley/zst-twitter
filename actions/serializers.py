from actions.models import Actions
from rest_framework import serializers

from authentication.models import User
from tweet.models import TweetMedia, Tweets

# Create your views here.
class TweetMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetMedia
        fields = ('media',)

class TweetSerializer(serializers.ModelSerializer):
    media_content = TweetMediaSerializer(many=True, read_only=True)


    class Meta:
        model = Tweets
        fields = ['id', 'content', 'media_content']
        depth = 1


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

class ActionSerializer(serializers.ModelSerializer):
    user = UserListSerializer(many=False, read_only=True)
    target = TweetSerializer(read_only=True)
    class Meta:
        model = Actions
        fields =('id','verb','user', 'target', 'created')