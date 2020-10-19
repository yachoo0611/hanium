from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.db.models import Count


def index(request):
    #twitter
    posts = Post.objects.all().filter(identifier=0).order_by('created_date')[:100]
    #dpost = Post.objects.all().annotate(Count('location', distinct=True))
    dposts = Post.objects.values('location').annotate(dcount=Count('location'))
    
    total = 0
    
    for dpost in dposts:
        total += dpost['dcount']

    print(total)
    tweet_posts = Post.objects.all().filter(identifier=0).order_by('-created_date')[:1]#트위터 가장 최근글
    tweet_counts = Post.objects.all().filter(identifier=0).order_by('title')
    images =  Post.objects.exclude(imageurl__isnull=True).exclude(imageurl__exact='').exclude(imageurl__exact=' ')#트위터 이미지 게시글

    # -----------------------------------------------------------------------------------------------------------
    posts2 = Post.objects.all().filter(identifier=1).order_by('created_date')[:100]
    # location_re = Post.objects.all.filter(location!='Unknown')
    facebook_posts = Post.objects.all().filter(identifier=1).order_by('created_date')[:1]
    facebook_counts = Post.objects.all().filter(identifier=1).order_by('title')

    return render(request, 'depandemic/index.html',
                  {'form': 'form', 'posts': posts, 'dposts': dposts, 'total': total, 'tweet_posts': tweet_posts,
                   'images': images, 'tweet_counts': tweet_counts,
                   'posts2': posts2, 'facebook_posts': facebook_posts, 'facebook_counts': facebook_counts})

    #return render(request, 'depandemic/index.html', {'form': 'form', 'posts': posts, 'dposts':dposts, 'total':total, 'tweet_posts':tweet_posts, 'images':images, 'tweet_counts': tweet_counts})

