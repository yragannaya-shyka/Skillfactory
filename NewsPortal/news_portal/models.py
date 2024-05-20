from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = self.post_set.aggregate(posts_rtng=Sum('rating'))['posts_rtng'] * 3
        comments_rating = self.user.comment_set.aggregate(comments_rtng=Sum('rating'))['comments_rtng']
        posts = self.post_set.all()
        posts_comments_rating = 0

        for post in posts:
            posts_comments_rating +=post.comment_set.aggregate(com_rt=Sum('rating'))['com_rt']

        self.rating  = posts_rating + comments_rating + posts_comments_rating
        self.save()
        return posts_rating + comments_rating + posts_comments_rating


class Category(models.Model):
    name = models.CharField(max_length=254, unique=True)


class Post(models.Model):

    article = "AR"
    news = "NW"

    POST_OPTIONS =[
        (article, "Статья"),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2,
                                 choices=POST_OPTIONS,
                                 default=article)
    public_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    topic = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

    def preview(self):
        self.preview = ''.join([self.content[:124], '...'])
        return self.preview


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    public_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()
