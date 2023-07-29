from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from notifications.signals import notify
import uuid
from django.urls import reverse


#==========Categorie Article ==============#

class ArticleSeries(models.Model):
    title = models.CharField(max_length=200) 
    slug = models.SlugField("Series slug", null=False, blank=False)
    published = models.DateTimeField("Date published", default=timezone.now)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Series"
        ordering = ['-published']


#================Article================#
class Article(models.Model):
    etat_choices = [
        ('accepted', 'accepted'),
        ('refused', 'refused'),
        ('panding', 'panding'),
    ]
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    article_slug = models.SlugField("Article slug", null=False, blank=False,unique=True)   #unique identifier for the Article
    content = RichTextField(blank=True, default="")
    published = models.DateTimeField("Date published", default=timezone.now)
    modified = models.DateTimeField("Date modified", default=timezone.now)
    etat = models.CharField( max_length=20, choices=etat_choices, default='panding')
    series = models.ForeignKey(ArticleSeries, default="", verbose_name="Series", on_delete=models.SET_DEFAULT)
    image  = models.ImageField(upload_to='article_images')


    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug': self.article_slug})

    @property
    def slug(self):
        return self.article_slug
    class Meta:
        verbose_name_plural = "Article"
        ordering = ['-published']

    def save(self, *args, **kwargs):
        if not self.article_slug:
            self.article_slug = str(uuid.uuid4())
        super().save(*args, **kwargs)
    @staticmethod
    def search(query, author=None):
        articles = Article.objects.filter(title__icontains=query)
        if author:
            articles = articles.filter(author=author)
        return articles

