from django import forms
from django.contrib.auth import(
    authenticate,get_user_model
)
User = get_user_model()
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length =120,widget = forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    def clean(self,*args,**kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username = username,password=password)
            if not user:
                raise forms.ValidationError('User does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Wrong password')
            if not user.is_active:
                raise forms.ValidationError("User does not active")
        return super(UserLoginForm,self).clean(*args,**kwargs)
class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length =120,widget = forms.TextInput)
    first_name = forms.CharField(max_length =120,widget = forms.TextInput)
    last_name = forms.CharField(max_length =120,widget = forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput)
    password1 = forms.CharField(min_length=8,max_length=30,widget = forms.PasswordInput)
    password2 = forms.CharField(widget = forms.PasswordInput)
    class Meta:
        model = User
        fields=[
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]
    def clean(self,*args,**kwargs):
        email = self.cleaned_data.get('email')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email_qs = User.objects.filter(email = email)
        username = self.cleaned_data.get('username')
        username_qs = User.objects.filter(username=username)
        if not password1 == password2:
            raise forms.ValidationError("Password didn't match")
        if email_qs.exists():
            raise forms.ValidationError('This email already exist')
        if username_qs.exists():
            raise forms.ValidationError('This username already exist')
        return super(UserRegisterForm,self).clean(*args,**kwargs)