from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, CustomUser, Hashtag
from .forms import PostForm, SigninForm, UserForm, CommentForm, HashtagForm

#from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse

# Create your views here.
def home(request):
    posts = Post.objects.all().order_by('-id')
    comment_form=CommentForm()
    return render(request, 'insta/home.html', {'posts':posts, 'comment_form':comment_form})

def loginn(request):
    signin_form=SigninForm()
    return render(request, 'insta/signin.html', {'signin_form': signin_form})

def sett(request):
    posts = Post.objects.all()
    return render(request, 'insta/sett.html', {'posts':posts})

def profile(request, user_id):
    # user=request.user
    # posts = Post.objects.filter(writer=user.pk).order_by('-id') #근데 이거는 html은 user.pk고 url은 <int:pk>이고 뷰스가 pk일때임.(return도 당근 필요)
    posts = Post.objects.all().filter(writer=user_id).order_by('-id')

    return render(request, 'insta/profile.html', {'posts':posts})

def mypage(request):
    posts = Post.objects.all()
    return render(request, 'insta/mypage.html', {'posts':posts})

def create(request):
    if not request.user.is_active:
        return HttpResponse("Can't write a post without Sign In")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.writer=request.user

            # location_field=form.cleaned_data['location_field']
            # str_locations=location_field.split('#')
            # list_locations=list()

            # for location in str_locations:
            #     location=location.strip()
            #     if Location.objects.filter(place=location):
            #         list_locations.append(Location.objects.get(place=location))
            #     else:
            #         temp_location=LocationForm().save(commit=False)
            #         temp_location.name=location
            #         temp_location.save()
            #         list_locations.append(temp_location)

            # post.save()
            # post.locations.add(*list_locations)


            hashtag_field=form.cleaned_data['hashtag_field']
            str_hashtags=hashtag_field.split('#')
            list_hashtags=list()

            for hashtag in str_hashtags:
                hashtag=hashtag.strip()
                if Hashtag.objects.filter(name=hashtag):
                    list_hashtags.append(Hashtag.objects.get(name=hashtag))
                else:
                    temp_hashtag=HashtagForm().save(commit=False)
                    temp_hashtag.name=hashtag
                    temp_hashtag.save()
                    list_hashtags.append(temp_hashtag)

            post.save()
            post.hashtags.add(*list_hashtags)

            #form.save_m2m()
            return redirect('home')
    else:
        form = PostForm()
        return render(request, 'insta/create.html', {'form': form})

def read(request):
    return redirect('home')

def update(request, pk):
    if not request.user.is_active:
        return HttpResponse("Can't write a post without Sign In")

    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form = form.save(commit=False)
            #post.hashtags.clear()
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)
        return render(request, 'insta/create.html', {'form': form})

def delete(request, pk):
    if not request.user.is_active:
        return HttpResponse("Can't write a post without Sign In")

    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('home')

def comment(request, post_id):
    if not request.user.is_active:
        return HttpResponse("Can't write a post without Sign In")

    post=get_object_or_404(Post, id=post_id)
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.c_writer=request.user
            comment.post_id=post
            comment.text=form.cleaned_data['text']
            comment.save()
            return redirect('home')

def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("로그인 실패. 다시 시도해보세요 ㅋ")


def signup(request):
    if request.method=="POST":
        form=UserForm(request.POST)
        if form.is_valid():
            new_user=CustomUser.objects.create_user(username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
            nickname=form.cleaned_data['nickname'],
            phone_number=form.cleaned_data['phone_number'])
            login(request, new_user)
            return redirect('home')
    else:
        form=UserForm()
        return render(request, 'insta/signup.html', {'form':form})

def hashtag(request, hashtag_name):
    hashtag=get_object_or_404(Hashtag, name=hashtag_name)
    return render(request, 'insta/hashtag.html', {'hashtag': hashtag})

# def location(request, location_place):
#     location=get_object_or_404(Location, name=location_place)
#     return render(request, 'insta/location.html', {'location': location})

def like(request, pk):
    if not request.user.is_active:
        return HttpResponse('First SignIn please')

    post=get_object_or_404(Post, pk=pk)
    user=request.user

    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return redirect('home')
