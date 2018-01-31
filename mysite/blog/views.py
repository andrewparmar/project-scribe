from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from django.views.generic import ListView
from .forms import EmailPostForms
from django.core.mail import send_mail

class PostListView(ListView):
    model = Post
    template_name = 'blog/post/post_list.html'


def post_list(request):
    object_list=Post.published.all()
    paginator = Paginator(object_list,3) # 3 posts per page
    page = request.GET.get('page')
    # print(request)
    try:
        print("Page: ", page)
        posts = paginator.page(page)
        print("posts: ", posts)
        print(dir(posts))
        for item in posts:
            print(item)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page':page,
                                                   'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == "POST":
        # Form was submitted
        form = EmailPostForms(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:

        ender(request, 'blog/post/share.html', {'post': post,
                                                        'form': form,
                                                        'sent': sent})