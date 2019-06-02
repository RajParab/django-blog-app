from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post, Comment
from .forms import EmailForm, CommentForm
from django.core.mail import send_mail

# Create your views here.

#This way we can represent each view using classes
# This is better than using fntion
class PostList(ListView):
	queryset=Post.published.all()
	context_object_name='posts'
	paginate_by=2
	template_name='blog/posts/list.html'



#views fro the website 
#How it looks on the browser

def post_list(request):
	objects=Post.published.all()
	#Paginator is used to make blogs into different pages
	paginator=Paginator(objects,2)#2 is the number of post in one page
	page=request.GET.get('page')
	try:
		posts=paginator.page(page)
	except PageNotAnInteger:
		#If page not a integer value
		posts=paginator.page(1)
	except EmptyPage:
		#if page is out of raange deleivver last page
		posts=paginator.page(paginator.num_pages)

	return render(request, "blog/posts/list.html",{'posts':posts,
													'page':page})

def post_details(request,year,month,day,posts):
	post=get_object_or_404(Post,slug=posts,
								publishTime__year=year,
								publishTime__month=month,
								publishTime__day=day)

	#list of active comments
	comments=post.comments.filter(active=True)
	new_comment=None

	if request.method=='POST': # then the comment is posted already
		comment_form=CommentForm(data=request.POST)

		if comment_form.is_valid():
			#if entered info is valid,
			# create comment obj but dont save it to database yet
			new_comment=comment_form.save(commit=False)

			#assign the current post to the comment
			new_comment.post=post

			#then save it to database
			new_comment.save()

	else: #Form is not filled yet
		comment_form=CommentForm()


	return render(request,'blog/posts/details.html',{'post':post,
													 'comments':comments,
													 'new_comment':new_comment,
													 'comment_form':comment_form})



def post_share(request, post_id):
	#retrieve post by id

	post=get_object_or_404(Post, id=post_id,status='published')
	sent= False

	if request.method=='POST':
		#Form was submitted

		form=EmailForm(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			post_url=request.build_absolute_uri(post.get_absolute_url())
			
			#The compolete mail to sent
			subject="%s (%s) recommends reading you %s" %(cd['name'],cd['email'],post.title)
			message="Do give the post :%s a read at %s \n\n on %s's recommendation: %s" %(post.title,post_url,cd['name'],cd['message'])

			#send the mail
			send_mail(subject, message, 'admin@blog.com', [cd['to']])
			sent = True

	else:
		form=EmailForm()

	return render(request, 'blog/posts/share.html', {'post':post,
														'form':form,
														'sent':sent,})