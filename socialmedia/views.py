from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.utils import timezone



# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages






@login_required
def dashboard(request):
    return render(request, "dashboard.html")