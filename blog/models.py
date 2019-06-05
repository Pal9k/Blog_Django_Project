from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length = 200)
    text = models.TextField()
    created_date = models.DateTimeField(default= timezone.now())
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    # name of this method should be same
    # this method defines where to go after posting the post
    # here we define to show the details of that particular post after posting it
    # DetailView needs primaryKey so kwargs is sended with pk !!!
    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    # this method defines once user done typing the comment
    # the user is taken to the list of all post_list
    # hence we can`t take user to detail of approve_comments
    # cause comments first need to approve by the admin weather want to show that comment or not
    # this will be listView and it will be homepage !!!!
    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text
