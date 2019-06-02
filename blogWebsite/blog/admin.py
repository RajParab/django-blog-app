from django.contrib import admin

# Register your models here.
from .models import Post, Comment

@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
	list_display=('title','slug', 'author','publishTime','status')
	list_filter=('author','publishTime','status')
	search_fields=('title','body')
	prepopulated_fields={'slug':('title',)}
	raw_id_fields=('author',)
	date_hiearchy='publishTime'
	ordering=('status','publishTime')

#Comment

@admin.register(Comment)

class CommentAdmin(admin.ModelAdmin):
	list_display=('name','emailID', 'comment', 'posted', 'updated','active')
	list_filter=('name','posted','active','updated')
	search_fields=('name','comment')