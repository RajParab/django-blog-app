from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse




class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,self).get_queryset()\
											.filter(status='published')



class Post(models.Model):

	#
	def get_absolute_url(self):
		return reverse('blog:post_details',
						args=[self.publishTime.year,
							self.publishTime.month,
							self.publishTime.day,
							self.slug
							])

	objects=models.Manager()

	published=PublishedManager() #New manager


	STATUS_CHOICES=(
		('draft','Draft'),
		('published','Published')
	)

	title=models.CharField(max_length =200)
	slug=models.CharField(max_length=200,unique_for_date="publishTime")
	author=models.ForeignKey(User,on_delete=models.CASCADE)
	emailID=models.EmailField(max_length=254)
	body=models.TextField()
	publishTime=models.DateTimeField(default=timezone.now)
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now_add=True)
	status=models.CharField(max_length=20,choices=STATUS_CHOICES,
												default='draft')

	class Meta:
		ordering=('-publishTime',)

	def __str__(self):
		return self.title


# Adding comments

class Comment(models.Model):
	post=models.ForeignKey(Post,
							on_delete=models.CASCADE, related_name='comments')
	name=models.CharField(max_length=20)
	emailID=models.EmailField(max_length=254)
	comment=models.TextField()
	posted=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now_add=True)
	active=models.BooleanField(default=True)

	class Meta:
		ordering=('posted',)

	def __str__(self):
		return 'Comment on %s by %s' %(self.post, self.name)