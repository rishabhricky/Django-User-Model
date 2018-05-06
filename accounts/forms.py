from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import RegexValidator

# from .models import MyUser (OR)
from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
from .models import USERNAME_REGEX
User = get_user_model()

"""
Commenting out the code so that I can have both the codes for:
    - Logining in with username or email
    - Login with email

To Reset password/ email activation use third party packages like
 - django registration redux
 - django all auth
 - python social auth

 joincfe.com/projects
"""


class UserLoginForm(forms.Form):
    username = forms.CharField(label='username / Email',)
    #     validators=[
    #         RegexValidator(
    #             regex = USERNAME_REGEX,
    #             message = 'Username must be alphanumeric or contain any of the following:". @ + -"',
    #             code = 'invalid_username',
    #         )],
    # )
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        # user_qs1 = User.objects.filter(username__iexact=username)
        # user_qs2 = User.objects.filter(email__iexact=username)
        # user_qs_final = (user_qs1 | user_qs2).distinct()

        # Above queries hit database twice which can be done in one
        # statment using Q
        user_qs_final = User.objects.filter(
            Q(username__iexact=username)|
            Q(username__iexact=username)
        ).distinct()

        if not user_qs_final.exists() and user_qs_final.count() != 1:
            raise forms.ValidationError("Invalid credentails -- user not exist")

        user_obj = user_qs_final.first()
        # user_obj = User.objects.filter(username=username).first()
        # the_user = authenticate(username=username, password=password)
        # if not the_user:
        #     raise forms.ValidationError("Invalid credentails!")

        # Below lines are how authentication works
        if not user_obj:
            raise forms.ValidationError("Invalid credentails -- Username invalid")
        else:
            if not user_obj.check_password(password):
                raise forms.ValidationError("Invalid credentails -- Invalid Password ")

        if not user_obj.is_active:
                    raise forms.ValidationError("Inactive user. Please verify your email address")

        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)

    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     user_qs = User.objects.filter(username=username).exists()
    #     user_exists = user_qs.exists()
    #     if not user_exists and user_qs.count() !=1:
    #         raise ValidationError("Invalid credentials")
    #     return username

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        # Create a new user hash for activating email
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
