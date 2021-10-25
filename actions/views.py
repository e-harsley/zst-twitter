from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView
from actions.serializers import ActionSerializer
from actions.models import Actions

class ActivitiesApi(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        actions = Actions.objects.exclude(user = request.user)
        following_ids = request.user.following.values_list('id',
                                                           flat=True)
        if following_ids:
            actions = actions.filter(user_id__in=following_ids)
            actions = actions.select_related('user') \
                          .prefetch_related('target')
            serializer = ActionSerializer(actions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'No activities'},status=status.HTTP_200_OK)

