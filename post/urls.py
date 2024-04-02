from django.urls import path

from .views import *




urlpatterns = [
    path('', PostListAPIView.as_view()),
    path('create/', PosCreateAPIView.as_view()),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('<uuid:id>/comments/', PostCommentListAPIView.as_view()),
    path('<uuid:pk>/likes/', LikesListAPIView.as_view()),
    path('<uuid:pk>/likes/create/', LikesCreateAPIView.as_view()),
    path('<uuid:pk>/comments/create/', PostCommentCreateAPIView.as_view()),
    path('<uuid:pk>/comments/likes/', CommentLikesListAPIView.as_view()),
    
    path('comments/', CommentsListCreateAPIView.as_view()),
    path('comments/<uuid:pk>/', CommentsRetreiveCreateAPIView.as_view()),
    path('likes/', LikesListCreateAPIView.as_view()),
]





