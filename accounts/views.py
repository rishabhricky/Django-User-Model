from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login, get_user_model, logout

# Create your views here.
from .forms import UserCreationForm, UserLoginForm
User = get_user_model()


def home(request):
    if request.user.is_authenticated():
        print(request.user.profile.city)
    return render(request, "base.html", {})

def register(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    # import pdb; pdb.set_trace()
    if form.is_valid():
        form.save()
        print("User created!")
        return HttpResponseRedirect("/login")
    return render(request, "accounts/register.html", {'form':form})


def login_view(request, *args, **kwargs):

    form = UserLoginForm(request.POST or None)
    # import pdb; pdb.set_trace()
    if form.is_valid():
        # form.save()
        username_ = form.cleaned_data.get('username')
        user_obj_ = User.objects.get(username__iexact=username_)
        login(request, user_obj_)
        print("User created!")
        return HttpResponseRedirect("/")
    return render(request, "accounts/login.html", {'form':form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login")
