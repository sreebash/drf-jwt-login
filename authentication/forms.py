from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password didn't match!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'Email', 'placeholder': 'Email address'}))
    first_name = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    password1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Password'}), label='Password')
    password2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Password (again)'}), label='Password (again)')

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'

        ]

    def clean(self):
        error_message = {
            'duplicate_email': 'Email is already taken'
        }
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(error_message['duplicate_email'], code='duplicate_email')
        except User.DoesNotExist:
            return self.cleaned_data


class UserLoginForm(forms.Form):
    email = forms.CharField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'Email address', 'required': True}))
    password = forms.CharField(label='Password', widget=forms.TextInput(
        attrs={'class': 'form-control', 'type': 'password', 'placeholder': 'Password', 'required': True}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user_qs_final = User.objects.filter(Q(email__iexact=email)).distinct()
        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("User does not exist")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError('Credentials are not correct!')
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)
