from django.contrib import admin
from .models import Article , ArticleSeries

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'article_slug', 'etat', 'published')

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleSeries)