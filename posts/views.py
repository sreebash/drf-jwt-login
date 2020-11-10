from django.shortcuts import render
import requests


# POSTS VIEW ENDPOINT

def posts(request):
    data = requests.get('https://jsonplaceholder.typicode.com/posts')
    posts = data.json()
    print(posts)
    return render(request, 'blog-listing.html', {'posts': posts})


# POST DETAILS VIEW ENDPOINT
def post_details(request, post_id):
    post_data = requests.get('https://jsonplaceholder.typicode.com/posts/1')
    post = post_data.json()

    print(post)
    data = requests.get('https://jsonplaceholder.typicode.com/posts/1/comments')
    comments = data.json()
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'blog-post.html', context=context)


