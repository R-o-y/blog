from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import redirect


def display_home_page(request):
    # return render(request, "home/home_page.html")
    return redirect("post/index")
