import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post



class LatesPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'New Posts Of My Blog'


    def items(self):
        return Post.published.all()[:5]
    
    def itme_title(self , item):
        return item.title
    
    def item_description(self , item):
        return truncatewords_html(markdown.markdown(item.content), 15)
    
    def item_pubdate(self , item):
        return item.publish