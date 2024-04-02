from django.shortcuts import render
from .models import Post, PostComment, PostLike, CommentLike
from .serializers import PostSerializer, PostCommentSerializer, CommentLikeSerializer, PostLikeSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from shared.pagination import CustomPagination
from rest_framework.response import Response




class PostListAPIView(ListAPIView):
    
    permission_classes = [permissions.AllowAny,]
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Post.objects.all()
    


class PosCreateAPIView(CreateAPIView):
    
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
        
        
class PostListCreateAPIView(ListCreateAPIView):
    
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):

    permission_classes = [permissions.AllowAny,]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    

    def put(self, request, *args, **kwargs):
        post = self.get_object()
        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'request status' : 'ok 200',
                'message': serializer.data
            }
        )

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        post.delete()
        return Response(
            {
                'request status' : 'ok 200',
                'message': "request has been deleted!"
            }
        )



class PostCommentListAPIView(ListAPIView):
    
    permission_classes = [permissions.AllowAny,]
    serializer_class = PostCommentSerializer
    
    def get_queryset(self):
        post_id = self.kwargs['id']
        queryset = PostComment.objects.filter(post__id = post_id)
        return queryset



class PostCommentCreateAPIView(CreateAPIView):
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(author=self.request.user, post_id=post_id)



class CommentsListCreateAPIView(ListCreateAPIView):
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    
    # def get_queryset(self):
    #     return self.queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    

class LikesListCreateAPIView(ListCreateAPIView):
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
        
        
        
class LikesListAPIView(ListAPIView):
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    serializer_class = PostLikeSerializer
    
    def get_queryset(self):
        post_id = self.kwargs["pk"]
        return PostLike.objects.filter(post_id=post_id)



class LikesCreateAPIView(CreateAPIView):
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    serializer_class = PostLikeSerializer
    
    def get_queryset(self):
        post_id = self.kwargs["pk"]
        return PostLike.objects.filter(post_id=post_id)
    
    def perform_create(self, serializer):
        post_id = self.kwargs["pk"]
        serializer.save(author=self.request.user, post_id=post_id)
        
        
        
        
        
        
        
        
        
        
        
        
        
        