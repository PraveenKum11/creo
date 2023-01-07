from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponseRedirect,
)
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator

from main.management.commands.image_generator import Photo
from main import (
    models,
    forms,
)
from cauth import forms as cauth_forms
import datetime
import calendar

# Create your views here.

def index(request):
    # Controller part (Logic Part)

    # NOTE : Queries are run lazily, so they are not run until the value needed
    #        and therefore we can sort it here itself.
    #        -> to order in reverse order add '-' in front on the column name
    trending_articles = models.Article.objects \
        .all() \
        .order_by("-likes")[:2]
    recent_articles = models.Article.objects \
        .all() \
        .order_by("-created_at")
    
    paginator = Paginator(recent_articles, 2)
    page_number = request.GET.get("page")
    page_articles = paginator.get_page(page_number)

    all_articles = models.Article.objects.order_by("created_at")

    context = {
        "trending_articles" : trending_articles,
        "recent_articles" : page_articles,
        "all_articles" : all_articles,
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

    if request.user.is_authenticated and article.likes.all().contains(request.user):
        context["liked"] = True

    return render(request, "main/article_details.html", context)

@login_required(login_url="/auth/login")
def create_article(request):
    article_form = forms.Article()

    if request.method == "POST":
        article_form = forms.Article(request.POST)
        tag = models.Tag.objects.get(pk = request.POST["tag"])

        thumbnail = Photo(type="Article", query=tag.name)
        thumbnail.create_photo()

        if article_form.is_valid():
            new_article = {
                "title" : request.POST["title"],
                "content" : request.POST["content"],
                "tag" : tag,
                "user" : request.user,
                "thumbnail" : thumbnail.path,
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
    article_form = forms.Article(initial=form_init)

    context = {
        "article_form" : article_form,
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

def tag_list(request, pk):
    tag = models.Tag.objects.get(pk = pk)
    article_list = tag.article_set.all()

    context = {
        "article_list" : article_list,
        "tag" : tag,
    }

    return render(request, "main/tag_list.html", context)


def article_archive(request, year, month):
    start_date = datetime.date(year, month, 1)
    end_date = datetime.date(year, month, calendar.monthrange(year, month)[1])
    article_list = models.Article.objects.filter(created_at__range=(start_date, end_date))

    context = {
        "year" : year,
        "month" : month,
        "article_list" : article_list,
    }

    return render(request, "main/article_archive.html", context)


def get_profile(request, pk):
    user = get_object_or_404(models.User, pk = pk)
    context = {
        "profile" : user.profile,
    }

    return render(request, "main/profile.html", context)

def edit_profile(request, pk):

    if request.method == "POST":
        u_form = cauth_forms.UserUpdateForm(request.POST, instance=request.user)
        p_form = forms.ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your Account has been updated!")

            return HttpResponseRedirect(reverse(get_profile, kwargs={"pk" : pk}))

    u_form = cauth_forms.UserUpdateForm(instance=request.user)
    p_form = forms.ProfileUpdateForm(instance=request.user.profile)

    context = {
        "u_form" : u_form,
        "p_form" : p_form,
    }

    return render(request, "main/edit_profile.html", context)