from django.shortcuts import render,redirect
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
)
from .forms import(
    UserLoginForm,
    UserRegisterForm,
)
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from todopost.tasks import signup_mail
def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = username,password = password)
        login(request,user)
        if next:
            return redirect(next)
        return redirect('/')
    context = {'form': form}
    return render(request,'acc/login.html',context)
def signup_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        new_user = authenticate(username = user.username,password = password)
        login(request,new_user)
        signup_mail.delay(new_user.pk)
        if next:
            return redirect(next)
        return redirect('home')
    context = {'form': form}
    return render(request,'acc/signup.html',context)

def logout_view(request):
    logout(request)
    return redirect('home')

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request,'acc/password_change.html',{'form':form})