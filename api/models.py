from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.
class Like(models.Model):
    id = models.BigAutoField(primary_key=True)
    tag = models.CharField(max_length=20)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(User,  models.SET_NULL, blank=True, null=True)
    created_date = models.DateField(null=True)
    updated_date = models.DateField(null=True)    

    def __str__(self):
        return self.tag

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Post(models.Model):
    LIST_OF_TYPE_POST = (
        ('Private', 'Private'),
        ('Public', 'Public')
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120)
    post_content = models.TextField()   
    post_type = models.CharField(max_length=40, choices=LIST_OF_TYPE_POST)
    tags = GenericRelation(Like)
    link = models.SlugField(default="", null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField()
    date_updated = models.DateField(null=True)

    @property
    def username(self):
        return self.user.username

    class Meta:  
        db_table = "posts"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.TextField(default='Without comment')
    tags = GenericRelation(Like)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField()
    date_updated = models.DateField(null=True)

    class Meta:  
        db_table = "comments"


class Share(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, related_name='shares', on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, related_name='shareduser', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField()
    date_updated = models.DateField(null=True)

    class Meta:  
        db_table = "shares"