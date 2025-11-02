from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import userPicturesForm
from .models import userPictures, userProfile, bookmarkImages
from django.contrib.auth import get_user_model
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Q
import json


#sign in page
def main(request):

    if request.user.is_authenticated:
        return redirect('homepage')

    if request.method == 'POST':
        User = get_user_model()
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        print(user)
        if user:
            authenticate_user = authenticate(request, username=user.username, password=password)
            print(authenticate_user)
            if authenticate_user:
                login(request, user)
                return redirect('homepage')
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('index')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('index')
    
    return render(request, 'index.html')

def signup(request):

    if request.user.is_authenticated:
        return redirect('homepage')
    
    if request.method == 'POST':
        User = get_user_model()
        username = request.POST.get('name')
        password = request.POST.get('pass')
        email = request.POST.get('email')
        repeat_password = request.POST.get('re_pass')
        if password != repeat_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        
        user = User.objects.filter(username=username, password=password, email=email).first()
        if user:
            messages.error(request, 'Account already exists')
            return redirect('signup')
        else:
            new_user = User.objects.create_user(username=username, password=password, email=email)
            login(request, new_user)
            return redirect('homepage')

    return render(request, 'sign_up.html')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def home_page(request):

    query = request.GET.get('search', '')
    if query == '':
        user_pictures = userPictures.objects.all().order_by('-upload_date')
    else:
        user_pictures = userPictures.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).order_by('-upload_date') if query else None

    if request.method == 'POST':
        form = userPicturesForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.uploader = request.user
            picture.save()
            messages.success(request, 'Image and title posted!')
            return redirect('homepage')
    else:
        form = userPicturesForm()

    page = request.GET.get('page', 1)
    paginator1 = Paginator(user_pictures, 15)
    try:
        numbers = paginator1.page(page)
    except PageNotAnInteger:
        numbers = paginator1.page(1)
    except EmptyPage:
        numbers = paginator1.page(paginator1.num_pages)

    bookmarks_ids = list(bookmarkImages.objects.filter(user=request.user).values_list('image_id', flat=True))
    print(bookmarks_ids)

    return render(request, 'dashboard/dashboard.html',{'form':form, 'numbers':numbers, 'bookmark_lists': bookmarks_ids})

@login_required
def get_img_data(request):

    img_id = request.GET.get('id')
    img_data = userPictures.objects.filter(id=img_id).first()
    data = model_to_dict(img_data)
    if img_data.uploader:
        data['uploader'] = img_data.uploader.username
    if img_data.image:
        data['image'] = img_data.image.url
    if img_data.upload_date:
        data['upload_date'] = img_data.upload_date.strftime('%Y-%m-%d %I:%M %p')
    if img_data.uploader.profile.profile_picture:
        data['uploader_profile_picture'] = img_data.uploader.profile.profile_picture.url

    return JsonResponse(data)

@login_required
def image_edit(request, id):   

    if request.method == 'POST':
        userImages = userPictures.objects.filter(id=id).first()

        previous_url = request.META.get('HTTP_REFERER')

        newTitle = request.POST.get('newTitle')
        newdescription = request.POST.get('newdescription')
        newImage = request.FILES.get('newImage', None)

        prevUserImage = userImages.image.url
        userImages.title = newTitle
        userImages.image = newImage if newImage else userImages.image
        userImages.description = newdescription
        userImages.save()
        os.remove('.' + prevUserImage) if newImage else None

        messages.success(request, 'Image and title updated successfully!')
        
        return redirect(previous_url)
        
    return redirect('homepage')

@login_required
def image_delete(request, id):

    if request.method == 'POST':
        previous_url = request.META.get('HTTP_REFERER')

        if id == 0:
            messages.error(request, 'Sorry! Something went wrong...')
            return redirect(previous_url)
        else:
            userImages = userPictures.objects.filter(id=id).first()
            prevUserImage = userImages.image.url
            userImages.delete()
            os.remove('.' + prevUserImage)
            messages.success(request, 'Post deleted successfully!')

            return redirect(previous_url)
    messages.success(request, 'Sorry! Something went wrong...')

    return redirect('homepage')


@login_required
def user_profile(request, username):
    User = get_user_model()
    user = User.objects.filter(username=username).first()
    if not user:
        messages.error(request, 'User does not exist')
        return redirect('homepage')

    user_pictures = userPictures.objects.filter(uploader=user).order_by('-upload_date')
    bookmarks_ids = list(bookmarkImages.objects.filter(user=user).values_list('image_id', flat=True))
    bookmark_posts = userPictures.objects.filter(bookmark__user_id=user).order_by('-bookmark__bookmarked_at')

    page = request.GET.get('page', 1)
    page2 = request.GET.get('page2', 1)
    paginator = Paginator(user_pictures, 5)
    bookmark_paginator = Paginator(bookmark_posts, 5)
    try:
        pins_per_page_numbers = paginator.page(page)
        bookmarked_pins_per_page_numbers = bookmark_paginator.page(page2)
    except PageNotAnInteger:
        pins_per_page_numbers = paginator.page(1)
        bookmarked_pins_per_page_numbers = bookmark_paginator.page(1)
    except EmptyPage:
        pins_per_page_numbers = paginator.page(paginator.num_pages)
        bookmarked_pins_per_page_numbers = bookmark_paginator.page(bookmark_paginator.num_pages)

    return render(request, 'dashboard/user_profile.html', {'profile_user': user, 'user_pictures': user_pictures, 'pins_per_page': pins_per_page_numbers, 'bookmark_lists': bookmarks_ids,
                                                           'bookmark_posts': bookmarked_pins_per_page_numbers
                                                           })


@login_required
def bookmarkImage(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        image_id = data.get('image_id')
        image_uploader = data.get('image_uploader')
        User = get_user_model()
        user = User.objects.filter(username=image_uploader).first()
        image = userPictures.objects.filter(id=image_id, uploader=user).first()
        if not image:
            return JsonResponse({'status': 'error', 'message': 'Image does not exist'}, status=400)
        
        bookmark, created = bookmarkImages.objects.get_or_create(user=request.user, image=image)
        if created:
            return JsonResponse({'status': 'success', 'message': 'Image bookmarked', 'button': 'Bookmarked!'})
        else:
            bookmark.delete()
            return JsonResponse({'status': 'success', 'message': 'Bookmark removed', 'button': 'Bookmark Image'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def edit_user_profile(request, username):
    User = get_user_model()
    user = User.objects.filter(username=username).first()

    userprofile = userProfile.objects.filter(user=user).first()
    previous_url = request.META.get('HTTP_REFERER')
    
    if not user:
        messages.error(request, 'User does not exist')
        return redirect('homepage')

    if request.method == 'POST':
        new_username = request.POST.get('username', userprofile.user.username)
        new_email = request.POST.get('email', userprofile.user.email)
        new_bio = request.POST.get('bio', userprofile.about)
        new_pic = request.FILES.get('new_profile_picture', userprofile.profile_picture)
        new_banner = request.FILES.get('banner_image', userprofile.banner_picture)
        previous_url = request.META.get('HTTP_REFERER')

        userprofile.user.username = new_username
        user.email = new_email
        userprofile.about = new_bio
        os.remove('.' + userprofile.profile_picture.url) if userprofile.profile_picture and new_pic != userprofile.profile_picture else None
        os.remove('.' + userprofile.banner_picture.url) if userprofile.banner_picture and new_banner != userprofile.banner_picture else None
        userprofile.profile_picture = new_pic if new_pic != userprofile.profile_picture else userprofile.profile_picture
        userprofile.banner_picture = new_banner if new_banner != userprofile.banner_picture else userprofile.banner_picture
        userprofile.save()
        user.save()

        return redirect(previous_url)

    return render(request, 'dashboard/user_profile/edit_profile.html', {'profile_user': user, 'previous_url': previous_url})

@login_required
def download_image(request, id):

    user_pictures = userPictures.objects.filter(id=id).first()

    response = HttpResponse(user_pictures.image, content_type='application/force-download')
    response['Content-Disposition'] = f"attachment; filename='{user_pictures.image.name}'"
    return response

@login_required
def delete_user(request, id):
    
    if request.method == 'POST':

        logout(request)

        user = get_user_model()
        user_to_delete = user.objects.filter(id=id).first()

        try:
            user_to_delete.delete()
        except user.DoesNotExist:
            messages.error(request, "User does not exist")    
            return redirect('homepage')

        return redirect('index')
    
    return redirect('homepage')

# Create your views here.
