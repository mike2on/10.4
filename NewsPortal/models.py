from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.urls import reverse
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect
User = get_user_model()



class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.FloatField(default=0.0)

    def update_rating(self):
        post_rating = self.post_set.all().aggregate(postRating=Sum('rating'))
        post_rate = 0
        post_rate += post_rating.get('postRating')

        comment_rating = self.user.comment_set.all().aggregate(commentRating=Sum('rating'))
        comment_rate = 0
        comment_rate += comment_rating.get('commentRating')

        self.author_rating = post_rate * 3 + comment_rate
        self.save()

    def __str__(self):
        return f"{self.user}"


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, related_name="categories")

    def __str__(self):
        return f"{self.category_name}"


news = 'NE'
article = 'AR'

POSITIONS = [(news, 'Новость'),
             (article, 'Статья')
             ]


class Post(models.Model):
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_choice = models.CharField(max_length=2, choices=POSITIONS)
    post_time_in = models.DateTimeField(auto_now_add=True)
    post_link = models.ManyToManyField(Category, "PostCategory")
    post_header = models.CharField(max_length=255)
    post_text = models.TextField()
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.post_text[0:128] + '...'



    def __str__(self):
        dataf = 'Post from {}'.format(self.post_time_in.strftime('%d.%m.%Y %H:%M'))
        return f"{dataf},{self.post_author},{self.post_header}"

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post_link = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_link = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.post_link},from the category:  {self.category_link}"


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time_in = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"{self.comment_time_in}, {self.comment_user}"

