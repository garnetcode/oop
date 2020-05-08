from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Profile
from django.core.files import File
from PIL import Image
from io import BytesIO
import os


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            directory = str(os.getcwd()) + "/media/"
            Profile.objects.filter(username=str(form.cleaned_data['username'])).update(picture=
                                                                                       fix(str(form.cleaned_data[
                                                                                                   'username']), str(
                                                                                           form.cleaned_data[
                                                                                               'picture']), directory))
            username = form.cleaned_data.get('username')
            messages.add_message(request, messages.SUCCESS, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def fix(username, image, location):
    def_loc = location
    default = Image.open(def_loc + "default.jpg")
    bckup = default
    thumb_io = BytesIO()
    default.save(thumb_io, 'JPEG', quality=85)
    default_thumbnail = File(thumb_io, name="profiles/" + username + image[-4:])
    location += "profiles/"
    try:
        os.renames(location + image, location + username + image[-4:])
    except FileNotFoundError:
        os.renames(location[:-7]+image, location+username+image[-4:])

    img = Image.open(location + username + image[-4:])
    if img.height > 300 or img.width > 300:
        basewidth = 300
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
        img.save(location + username + image[-4:])
        img.close()
        img = Image.open(location + username + image[-4:])
        thumb_io = BytesIO()
        try:
            img.save(thumb_io, 'JPEG', quality=85)
            thumbnail = File(thumb_io, name="/profiles/"+username+image[-4:])
            bckup.save(def_loc + "default.jpg")
            return thumbnail
        except OSError:
            bckup.save(def_loc + "default.jpg")
            return default_thumbnail
    bckup.save(def_loc + "default.jpg")
    return default_thumbnail
