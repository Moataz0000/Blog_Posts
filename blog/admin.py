from django.contrib import admin
from .models import Post , Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title' , 'slug' , 'auther' , 'publish' , 'status' ]
    list_filter = ['status' , 'created' , 'publish' , 'auther']
    search_fields = ['title' , 'content']
    prepopulated_fields = {'slug':('title',)}
    # raw_id_fields = ['auther']
    date_hierarchy = 'publish'
    ordering = ['status' , 'publish']


    
@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post','created' , 'active']
    list_filter = ['active' , 'created', 'updated']
    search_fields = ['name' , 'email', 'content']
