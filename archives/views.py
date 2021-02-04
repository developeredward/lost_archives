from django.shortcuts import render, redirect, reverse, HttpResponse
from django.db.models import Count, Q
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from django.core.paginator import Paginator
from .models import Author, Post, Category, PostView
from .forms import CommentForm
from subscription.forms import EmailSignupForm
from subscription.models import Signup

form = EmailSignupForm()

# Create your views here.

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

    context = {
        'queryset': queryset
    }


    return render(request, 'search_results.html', context)


def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset

def index(request):
    latest = Post.objects.order_by('-timestamp')[0:3]
    context = {
        'latest': latest,
    }

    return render(request, 'index.html')

class IndexView(View):
    form = EmailSignupForm()
    def get(self, request, *args, **kwargs):
       latest = Post.objects.order_by('-timestamp')[0:3]
       most_read = Post.objects.order_by('-comments')[0:3]
       context = {
           'latest' : latest,
           'most_read': most_read,
           'form': self.form
       }
       return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        messages.info(request, "Successfully subscribed")
        return redirect("home")

class PostListView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'queryset'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        queryset = Post
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'
    context_object_name = 'post'
    paginate_by = 1
    form = CommentForm

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-details", kwargs={
                'pk': post.pk
            }))
