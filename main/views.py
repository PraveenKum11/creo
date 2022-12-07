from django.shortcuts import (
    render,
    get_object_or_404,
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

from main import (
    models,
    forms,
)

# Create your views here.

def index(request):
    # Controller part (Logic Part)

    # NOTE : Queries are run lazily, so they are not run until the value needed
    #        and therefore we can sort it here itself.
    #        -> to order in reverse order add '-' in front on the column name
    trending_articles = models.Article.objects \
        .all() \
        .order_by("-likes")[:6]
    latest_articles = models.Article.objects \
        .all() \
        .order_by("-created_at")
    # tags = models.Article.objects \
    #     .values_list("tag", flat=True) \
    #     .distinct()
    tags = models.Tag.objects.all().distinct()

    context = {
        "trending_articles" : trending_articles,
        "latest_articles" : latest_articles,
        "tags" : tags,
    }

    return render(request, "main/index.html", context)

def article_details(request, pk):
    # This gives 500 error when article does not exist
    # To avoid this we can use try except or even better is get_object_or_404()

    # try:
    #     article = models.Article.objects.get(pk = pk)
    # except:
    #     raise Http404()
    article = get_object_or_404(models.Article, pk = pk)

    if request.method == "POST":
        comment_form = forms.Comment(request.POST)
        if comment_form.is_valid():
            commentor = comment_form.cleaned_data["commentor"]
            comment_content = comment_form.cleaned_data["comment_content"]

            article.comment.create(commentor = commentor, comment_content = comment_content)
            return HttpResponseRedirect(request.path_info)

    comment_form = forms.Comment()

    context = {
        "article" : article,
        "comment_form" : comment_form,
    }

    return render(request, "main/article_details.html", context)

def user_details(request, pk):
    # user = models.User.objects.get(pk = pk)
    user = get_object_or_404(models.User, pk = pk)

    context = {
        "user" : user,
    }

    return render(request, "main/user_details.html", context)

def tag_details(request, pk):
    tag = get_object_or_404(models.Tag, pk = pk)

    context = {
        "tag" : tag,
    }
    
    return render(request, "main/tag_details.html", context)

@login_required(login_url="/auth/login")
def create_article(request):
    article_form = forms.Article()

    if request.method == "POST":
        article_form = forms.Article(request.POST)

        # tag handeling
        tag = models.Tag.objects.get(pk = request.POST["tag"])

        if article_form.is_valid():
            new_article = {
                "title" : request.POST["title"],
                "content" : request.POST["content"],
                "tag" : tag,
                "user" : get_user_model().objects.get(pk = 1),
            }
            models.Article.objects.create(**new_article)
            return HttpResponseRedirect("/")

    context = {
        "article_form" : article_form,
        "user_name" : get_user_model().objects.get(pk = 1)
    }

    return render(request, "main/create_article.html", context)

@login_required(login_url="/auth/login")
def delete_article(request, pk):
    get_object_or_404(models.Article.objects, pk = pk).delete()
    return HttpResponseRedirect("/")

@login_required(login_url="/auth/login")
def edit_article(request, pk):
    article = models.Article.objects.get(pk = pk)
    edit_form = forms.Article(article)
    # print(article.)

    context = {
        "edit_form" : edit_form,
    }

    return render(request, "main/edit_article.html", context)