from django.shortcuts import render , HttpResponse
from .models import Blogpost

def index(request):
    blog = Blogpost.objects.all()
    return render(request,'blog/index.html',{'blog': blog})

def blogpost(request,id):
    post = Blogpost.objects.filter(post_id = id)[0]
    # print(post)
    return render(request,'blog/blogpost.html',{'post': post})

