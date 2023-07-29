from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from notifications.signals import notify
from Article.models import Article, ArticleSeries
from .models import Comment
from .forms import CommentForm
from django.shortcuts import redirect
from notifications.signals import notify
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def Home(request):
    latest_article = Article.objects.filter(
        etat="accepted", published__lte=timezone.now()
    ).order_by("-published")[:3]
    article_series = ArticleSeries.objects.all()
    series_articles = []
    for series in article_series:
        latest_articles = series.article_set.filter(
            etat="accepted", published__lte=timezone.now()
        ).order_by("-published")[:3]
        series_articles.append((series, latest_articles))

    paginator = Paginator(
        Article.objects.filter(etat="accepted").all(), 8
    )  # Change 10 to the desired number of articles per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "Magazine/home.html",
        {
            "latest_article": latest_article,
            "latest_articles": latest_articles,
            "article_series": article_series,
            "page_obj": page_obj,
            "series_articles": series_articles,
        },
    )


def category_page(request, slug):
    series = get_object_or_404(ArticleSeries, slug=slug)
    articles = Article.objects.filter(series=series)

    # Paginate the articles
    paginator = Paginator(articles, 6)  # Display 6 articles per page
    try:
        page_number = int(request.GET.get("page", 1))
    except ValueError:
        page_number = 1
    try:
        articles = paginator.page(page_number)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    article_series = ArticleSeries.objects.all()
    context = {
        "series": series,
        "articles": articles,
        "article_series": article_series,
    }
    return render(request, "Magazine/Categorie.html", context)


def is_authenticated(user):
    return user.is_authenticated


from django.http import HttpResponseRedirect
from django.urls import reverse


def add_comment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article

            if request.user.is_authenticated:
                comment.author = request.user
            else:
                return HttpResponseRedirect(reverse("sign"))

            comment.save()

            # Add a notification for the author of the article
            notify.send(
                request.user,
                recipient=article.author,
                verb="commented on your article",
                target=article,
            )

    else:
        form = CommentForm()
    article_series = ArticleSeries.objects.all()

    return render(
        request,
        "dashboard/Article/view_article.html",
        {"form": form, "article": article, "article_series": article_series},
    )


def searchMagazine(request):
    query = request.GET.get("q")

    articles = Article.search(query) if query else Article.objects.all()
    return render(
        request, "Magazine/search.html", {"articles": articles, "query": query}
    )


def error_404(request, exception):
    return render(request, "404.html", status=404)
