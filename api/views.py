from django.shortcuts import render

# Create your views here.
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics
from django.http import HttpResponse as Response
from rest_framework import status
from django.views import View
from django.contrib.auth.models import User
from django.db.models import Q, Count
from .models import (
    Post,
    Comment,
    Like,
    Share,
)
from datetime import date, datetime
# from rest_framework import permissions

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import (
    UserSerializer,
    PostSerializer,
    PostByLinkSerializer,
    LikeSerializer,
    CommentSerializer,
    ShareSerializer,
)

class UserViewData(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    # permission_classes = [permissions.IsAuthenticated]


# Multiple Posts
class getMultiplePostData(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all().annotate(
        count_likes=Count("tags", filter=Q(tags__tag='like')),
        count_loves=Count("tags", filter=Q(tags__tag='love')),
        count_sads=Count("tags", filter=Q(tags__tag='sad')),
        count_comments=Count("comments"),
        count_shares=Count("shares"),
        )[:12]


# Multiple Posts of specific user
class getPostDataByUser(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all().annotate(
        count_likes=Count("tags", filter=Q(tags__tag='like')),
        count_loves=Count("tags", filter=Q(tags__tag='love')),
        count_sads=Count("tags", filter=Q(tags__tag='sad')),
        count_comments=Count("comments"),
        count_shares=Count("shares"),
        )[:12]
    
    def get_queryset(self):
        username = self.kwargs['username']
        if username:
            self.queryset = Post.objects.filter(user__username=username).annotate(
                count_likes=Count("tags", filter=Q(tags__tag='like')),
                count_loves=Count("tags", filter=Q(tags__tag='love')),
                count_sads=Count("tags", filter=Q(tags__tag='sad')),
                count_comments=Count("comments"),
                count_shares=Count("shares"),
            )
            return self.queryset
        else:
            return self.queryset


# Data for Specific Post
class getPostDataByLink(viewsets.ModelViewSet):
    serializer_class = PostByLinkSerializer
    queryset = Post.objects.all().annotate(
        count_likes=Count("tags", filter=Q(tags__tag='like')),
        count_loves=Count("tags", filter=Q(tags__tag='love')),
        count_sads=Count("tags", filter=Q(tags__tag='sad')),
        count_comments=Count("comments"),
        count_shares=Count("shares"),
        )[:4]
    
    def get_queryset(self):
        link = self.kwargs['link']
        if link:
            self.queryset = Post.objects.filter(link=link).annotate(
                count_likes=Count("tags", filter=Q(tags__tag='like')),
                count_loves=Count("tags", filter=Q(tags__tag='love')),
                count_sads=Count("tags", filter=Q(tags__tag='sad')),
                count_comments=Count("comments"),
                count_shares=Count("shares"),
            )[:1]
            return self.queryset
        else:
            return self.queryset


class CommentModelViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):

        server_data = {'user': request.user.id, 'date_created': date.today(), 'date_updated': date.today()}
        comment_data = request.data

        serializer = self.serializer_class(data = { **server_data, **comment_data})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareModelViewSet(viewsets.ModelViewSet):
    serializer_class = ShareSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):

        server_data = {'user': request.user.id, 'date_created': date.today(), 'date_updated': date.today()}
        shared_with = request.data

        serializer = self.serializer_class(data = { **server_data, **shared_with})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
