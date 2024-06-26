from django.db import models
from users.models import User
from django.contrib.auth import get_user_model
from shared.models import BaseModel
from django.core.validators import FileExtensionValidator, MaxLengthValidator
from django.db.models import UniqueConstraint



class Post(BaseModel):
    '''title, author, body, post_image'''
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') # User.posts.all()
    body = models.TextField()
    post_image = models.ImageField(upload_to='post_images/', default='post_images/post_default.jpg', 
                                   validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])
    
    class Meta:
        db_table = "posts"
        verbose_name = "post"
        verbose_name_plural = "posts"
        
    def __str__(self):
        return self.title
    


class PostComment(BaseModel):
    '''author, post, comment, parent'''
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments") # Post.comments.all() all comments related one Post
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    def __str__(self):
        return self.comment



class PostLike(BaseModel):
    '''author, post'''
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['author', 'post'],
                name='postLikeUnique'
                )
            ]
        
    def __str__(self):
        return f"liked by {self.author}"
    


class CommentLike(BaseModel):
    '''author, comment'''
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(PostComment, on_delete=models.CASCADE, related_name="likes")
    
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['author', 'comment'],
                name='author_comment'
                )
            ]

        def __str__(self):
            return f"comment like by {self.author}"
