from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
import cloudinary.uploader
from tweet.serializers import TweetSerializer
from tweet.models import Tweets, TweetMedia
from rest_framework import permissions
from actions.utils import create_action


class TweetAPIView(APIView):
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        files = request.FILES.getlist('media_content')
        if files:
            request.data.pop('media_content')
            serializer = TweetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                tweet_query = Tweets.objects.get(pk = serializer.data['id'])
                upload_file_to_cloudinary = []
                for file in files:
                    cloud_upload = cloudinary.uploader.upload(file)
                    tweet_media = TweetMedia.objects.create(user=user, media=cloud_upload['url'])
                    upload_file_to_cloudinary.append(tweet_media)
                tweet_query.media_content.add(*upload_file_to_cloudinary)
                context = serializer.data
                context["media_content"] = [file.media for file in upload_file_to_cloudinary]
                create_action(user, 'tweeted', tweet_query)
                print('jsjdjd')
                return Response(context, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = TweetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                context = serializer.data
                return Response(context, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

