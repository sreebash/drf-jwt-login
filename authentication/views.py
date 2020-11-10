from django.contrib.auth import login, logout, get_user_model
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, permissions, mixins
from .serializers import UserAccountSerializer, UserSerializer

# LOGIN VIEW ENDPOINT

User = get_user_model()


def login_view(request):
    _next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            login(request, user_obj)
            if _next:
                return redirect(_next)
            return redirect('posts:index')
        return render(request, 'login.html', {'form': form})
    return render(request, 'login.html', {'form': form})


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            # instance = form.save(commit=False)
            # instance.is_active = False
            # instance.save()
            form.save()
            return redirect('authentication:login')
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


# Register API View
class RegisterApiView(generics.GenericAPIView):
    serializer_class = UserAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'email': UserSerializer(user, context=self.get_serializer_context()).data,
                         'message': 'User Created Successfully. Now perform login to get your token', })
