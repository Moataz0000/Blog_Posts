from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

app_name = 'blog'

sitemaps = {
    'posts':PostSitemap,
}
from .feeds import LatesPostsFeed
urlpatterns = [
    # F_B_V
    path('', views.list_of_posts , name='post_list'),
    path('tag/<slug:tag_slug>/' , views.list_of_posts , name='post_list_by_tag'),
    # URL For the Single post
    path('<int:year>/<int:month>/<int:day>/<slug:post>/' , views.post_details , name='post_detail'),
    # URL For share post with email 
    path('<int:post_id>/share/', views.post_share ,name='post_share'),
    # URL For commnets
    path('<int:post_id>/comment/', views.post_comment , name='post_comment'),
    # Sitemaps URL
    path('sitemap.xml', sitemap, {'sitemaps':sitemaps} , name='django.contrib.sitemaps.views.sitemap'),
    path('feed/' , LatesPostsFeed() , name='post_feed'),
    # Search URL
    path('search/' , views.post_search, name='post_search'),

]