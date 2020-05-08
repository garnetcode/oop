from django.shortcuts import render, redirect
from users.models import Profile
from .models import Article
from django.contrib import messages
from .forms import ModelArticle, Upvote
import os
from PIL import Image
from io import BytesIO
from django.core.files import File


def home(request):
    form = Upvote()
    if request.method == 'POST':
        if request.POST.get('upVote'):
            title = str(request.POST.get('upVote'))
            for article in Article.objects.all():
                if article.title.lower() == title.lower():
                    Article.objects.filter(title=article.title).update(votes=article.votes + 1)
                    if article.votes % 5 == 0:
                        Profile.objects.filter(username=article.author).update(
                            votes=[i.votes for i in Profile.objects.filter(username=article.author)][0] + 1)

                    break

        if request.POST.get('downVote'):
            title = str(request.POST.get('downVote'))
            for article in Article.objects.all():
                if article.title.lower() == title.lower():
                    if article.votes > 0:
                        Article.objects.filter(title=article.title).update(votes=article.votes - 1)
                        break

            print("Downvote " + request.POST.get('downVote'))
    """if request.user.is_authenticated:
        if request.user.username == 'admin':
            profile = {'username': request.user.username, 'picture': "/media/default.jpg"}
        else:
            profile = [{'picture': "/media/" + str(i.picture), 'username': i.username} for i in
                       Profile.objects.filter(username=request.user.username)][0]
    else:
        profile = {'username': 'Anonymous', 'picture': "/media/default.jpg"}
     """
    posts = [
        {'author': i.author, 'title': i.title.title(), 'content': i.content, 'date': i.date,
         'scene': "/media/" + str(i.scene), 'votes': i.votes}
        for i in Article.objects.all().order_by('-date')]

    context = {
        'form': form,
        'posts': posts,
    }
    return render(request, 'home.html', context)


def writers(request):
    profiles = [
        {'picture': "/media/" + str(i.picture), 'username': i.username, 'description': i.description, 'votes': i.votes}
        for i in
        Profile.objects.all().order_by('-votes')]
    context = {
        'profiles': profiles
    }
    return render(request, 'writers.html', context)


def check(request):
    if request.user.is_authenticated:
        return redirect('publish')
    else:
        return redirect('login')


def addStory(request):
    usr = request.user
    if request.method == 'POST':
        form = ModelArticle(data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            directory = str(os.getcwd()) + "/media/"
            Article.objects.filter(title=str(form.cleaned_data['title'])).update(scene=
                                                                                 fix(str(form.cleaned_data[
                                                                                             'title']), str(
                                                                                     form.cleaned_data[
                                                                                         'scene']), directory),
                                                                                 author=usr.username)
            title = form.cleaned_data.get('title')
            messages.add_message(request, messages.SUCCESS, f'{title} has been published!')
            return redirect('publish')
    else:
        form = ModelArticle()
    if request.user.is_authenticated:
        if request.user.username == 'admin':
            profile = {'username': request.user.username, 'picture': "/media/default.jpg"}
        else:
            profile = [{'picture': "/media/" + str(i.picture), 'username': i.username} for i in
                       Profile.objects.filter(username=request.user.username)][0]
    else:
        profile = {'username': 'Anonymous', 'picture': "/media/default.jpg"}
    username = "Anonymous"
    try:
        for i in Profile.objects.filter(username=request.user.username):
            username = i.username
            profile['username'] = username
            try:
                profile['picture'] = "/media/" + str(i.picture)
            except KeyError:
                profile['picture'] = "/media/default.jpg"

    except IndexError:
        profile = {'username': username, 'picture': "/media/default.jpg"}

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'content.html', context)


def fix(title, image, location):
    def_loc = location
    default = Image.open(def_loc + "default.jpg")
    backup = default
    thumb_io = BytesIO()
    default.save(thumb_io, 'JPEG', quality=85)
    default_thumbnail = File(thumb_io, name="news/" + title + image[-4:])
    location += "news/"
    try:
        os.renames(location + image, location + title + image[-4:])
    except FileNotFoundError:
        os.renames(location[:-5] + image, location + title + image[-4:])

    img = Image.open(location + title + image[-4:])
    if img.height > 300 or img.width > 300:
        basewidth = 300
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save(location + title + image[-4:])
        img.close()
        img = Image.open(location + title + image[-4:])
        thumb_io = BytesIO()
        try:
            img.save(thumb_io, 'JPEG', quality=85)
            thumbnail = File(thumb_io, name="/news/" + title + image[-4:])
            backup.save(def_loc + "default.jpg")
            return thumbnail
        except OSError:
            backup.save(def_loc + "default.jpg")
            return default_thumbnail
    backup.save(def_loc + "default.jpg")
    return default_thumbnail
