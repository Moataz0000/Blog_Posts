from django.shortcuts import render , get_object_or_404
from .models import Post , Comment
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.views.generic import ListView
from.forms import EmailPostForm , CommentForm , SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector , SearchQuery , SearchRank


# F_B_V 
def list_of_posts(request , tag_slug=None):
    posts_list = Post.published.all().order_by('-created')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag , slug=tag_slug) # git the tag object with the tag_slug 
        posts_list = posts_list.filter(tags__in=[tag])

    paginator = Paginator(posts_list , 3) # Here, we create a Paginator object named paginator with a page size of 3 posts per page.
    page_number = request.GET.get('page' , 1) # This line retrieves the value of the page parameter from the request's query string. If the parameter is not present, it defaults to 1.
    try:
       posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)  
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)     

    return render(request , 'blog/posts/list.html' ,{'posts':posts , 'tag':tag})


# C_B_V
# class PostListView(ListView):
#     """
#     Alternative Post List View
#     """
#     queryset = Post.published.all().order_by('-created')
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/posts/list.html'





def post_details(request , post , year , month , day):
    post = get_object_or_404(Post,status=Post.Status.PUBLISHED, publish__year=year , publish__month=month , publish__day=day,slug=post)
    # list of active comments for this post
    commetns = post.comments.filter(active=True)
    # form for users to comment
    form = CommentForm()

    # Tags
    post_tags_ids = post.tags.values_list('id' , flat=True) # retrive tubles with the value
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', 'publish')[:4]



    context = {
        'post':post,
        'form':form,
        'comments':commetns,
        'similar_posts': similar_posts,
    }
    return render(request, 'blog/posts/details.html', context)




def post_share(request , post_id):
    # retriver post by id 
    post = get_object_or_404(Post , id=post_id , status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST) # form was submitted 
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data # this is a dict of form fields and their values
            # ...send email
            post_url = request.build_absolute_uri(post.get_absolute_url()) # post url 
            subject = f"{cd['name']} recommends you read"\
                      f'{post.title}'
            message = f"Read {post.title} at {post_url}\n\n"\
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject , message , 'motazfawzy73@gmail' ,[cd['to']])
            sent = True
            
    else:
        form = EmailPostForm() # if method is GET to return Empty form
    context = {
        "form":form,
        'post':post,
        'sent':sent,
    }    
    return render(request , 'blog/posts/share.html' , context)            



# Only allow POST requests for this view
@require_POST
def post_comment(request , post_id):
    post = get_object_or_404(Post , id=post_id , status=Post.Status.PUBLISHED)
    comment = None

    # A comment Was Post
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # create a comment object without saveing it to the database
        comment = form.save(commit=False) 
        # Assign the post to the comment
        comment.post = post
        # save the comment to the database
        comment.save()
    context = {
        'form':form,
        'comment':comment,
        'post':post
    }    
    return render(request , 'blog/posts/comment.html' , context)






def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            search_vector = SearchVector('title', 'content', config='english') #search in model post and title and content fields
            search_qeuery = SearchQuery(query ,  config='english') # create object by query




            results = Post.published.annotate(
                search=search_vector,rank=SearchRank(search_vector,search_qeuery)
            ).filter(search=search_qeuery).order_by('-rank')
    context = {
        'form':form,
        'query':query,
        'results':results
    }        
    return render(request , 'blog/posts/search.html' , context)        