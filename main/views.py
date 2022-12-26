from django.shortcuts import (
    render,
    get_object_or_404,
)

from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
)
from django.urls import reverse
from django.contrib import messages

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

    # for handling comments 
    if request.method == "POST":
        comment_form = forms.Comment(request.POST)
        if comment_form.is_valid():
            commentor = request.user
            comment_content = comment_form.cleaned_data["comment_content"]

            article.comment.create(commentor = commentor, comment_content = comment_content)
            return HttpResponseRedirect(request.path_info)

    comment_form = forms.Comment()

    context = {
        "article" : article,
        "comment_form" : comment_form,
        "liked" : None
    }

    # print(type(request.user))
    # print(request.user)
    # if request.user != "AnonymousUser" and article.likes.all().contains(request.user):
    #     context["liked"] = True

    return render(request, "main/article_details.html", context)

"""
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
                "user" : get_user_model().objects.filter(username=request.POST["username"])[0],
            }
            models.Article.objects.create(**new_article)
            return HttpResponseRedirect("/")

    context = {
        "article_form" : article_form,
    }

    return render(request, "main/create_article.html", context)

@login_required(login_url="/auth/login")
def delete_article(request, pk):
    article = get_object_or_404(models.Article.objects, pk = pk)

    if article.user == request.user:
        article.delete()
    else:
        print("no no no")

    return HttpResponseRedirect("/")

@login_required(login_url="/auth/login")
def edit_article(request, pk):
    article = models.Article.objects.get(pk = pk)
    form_init = {
        "title" : article.title,
        "content" : article.content,
        "tag" : article.tag,
    }
    edit_form = forms.Article(initial=form_init)

    context = {
        "edit_form" : edit_form,
    }

    if request.method == "POST":
        # Updating the article with the new changes
        article.title = request.POST["title"]
        article.content = request.POST["content"]
        article.tag = models.Tag.objects.get(pk = request.POST["tag"])
        article.save()

        return HttpResponseRedirect(reverse(article_details, kwargs={"pk" : pk}))

    return render(request, "main/edit_article.html", context)

def like_article(request, pk):
    article = get_object_or_404(models.Article, pk = pk)
    user = request.user

    context = {
        "article" : article,
        "liked" : None,
    }

    if article.likes.all().contains(user):
        article.likes.remove(user)
        context["liked"] = None
    else:
        article.likes.add(user)
        article.save()
        context["liked"] = True

    return render(request, "main/partials/user_likes.html", context)

"""

def get_profile(request, pk):
    user = get_object_or_404(models.User, pk = pk)
    context = {
        "profile" : user.profile,
    }

    return render(request, "main/profile.html", context)