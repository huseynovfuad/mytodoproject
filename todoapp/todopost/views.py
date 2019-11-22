from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import JsonResponse
from .models import Post,Comment,Share
from .forms import CommentForm,PostForm,ShareForm
from datetime import datetime, timedelta
from .tasks import notification
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    posts = Post.objects.filter(share__with_user = request.user).order_by("-id")
    context = {
        'posts':posts,
    }
    return render(request,'home.html',context)


@login_required
def detail_view(request,post_id):
    post = Post.objects.filter(share__with_user = request.user).get(id=post_id)
    comments = Comment.objects.filter(post = post).order_by('-id')
    form = CommentForm(request.POST or None)
    context ={
        'post':post,
        'comments':comments,
        'form' : form
    }
    return render(request,'post_detail.html',context)


@login_required
def create_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        new_form = form.save(commit=False)
        new_form.author = request.user
        new_form.save()
        Share.objects.create(post = new_form,with_user = new_form.author)
        obj = Post.objects.filter(pk=new_form.pk).first()
        tomorrow = obj.finished - timedelta(minutes=10)
        notification.apply_async((new_form.pk,),eta=tomorrow)
        return redirect('home')
    context ={
        'form': form,
    }
    return render(request,'post_create.html',context)


@login_required
def post_share(request,post_id):
    post = Post.objects.get(id=post_id)
    form = ShareForm(request.POST or None)
    if form.is_valid():
        with_user_txt = form.cleaned_data.get('with_user')
        with_user = User.objects.filter(username = with_user_txt).first()
        if with_user is not None:
            Share.objects.create(post=post,with_user=with_user)
        else:
            print('This user doesnt exist')
        return redirect('home')
    return render(request,'post_share.html',{'form':form})

@login_required
def delete_post(request):
    id1 = request.GET.get('id')
    Post.objects.get(id=id1).delete()
    data = {
        'deleted':True
    }
    return JsonResponse(data)

@login_required
def update_post(request,post_id):
    post =Post.objects.get(id=post_id)
    form = PostForm(request.POST or None,instance=post)
    if form.is_valid():
        new_form=form.save()
        if new_form.author == request.user:
            new_form.save()
        else:
            print("This is not your post!")
        return redirect('home')
    return render(request,'post_update.html',{'form':form})

@login_required
def delete_comment(request):
    id1=request.GET.get('id',None)
    Comment.objects.get(id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)

@login_required
def comment_update(request,comment_id):
    comment = Comment.objects.get(id=comment_id)
    form = CommentForm(request.POST or None,instance=comment)
    if form.is_valid():
        new_form = form.save()
        print(comment.post.id)
        post_id = comment.post.id
        return HttpResponseRedirect("/post/" + str(post_id) +'/')
    return render(request,'post_detail.html',{'form':form})
