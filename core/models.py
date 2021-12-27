from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

STATUS_CHOICES=[
	('Pending','Pending'),
	('Approved','Approved'),
	('Reject','Reject'),
]

class Author(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_on']
		
	def __str__(self):
		return self.user.full_name


class Paper(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
	status = models.CharField(max_length=30,default='Pending')
	file = models.FileField(upload_to='author_files/') # taking files from author
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['created_on']
		
	def __str__(self):
		return self.title


class Reviewer(models.Model):
	user = models.OneToOneField(User,related_name='reviewer',on_delete=models.CASCADE)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)


	class Meta:
		ordering = ['-created_on']
		
	def __str__(self):
		return self.user.full_name

class PaperAssign(models.Model):
	review = models.ForeignKey(Reviewer,related_name='assigned_paper',on_delete=models.CASCADE)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	assign_paper = models.ForeignKey(Paper,on_delete=models.CASCADE)


	class Meta:
		ordering = ['-created_on']

	def __str__(self):
		return f'{self.review.user.full_name} - {self.assign_paper.title}'
# request.user.reviewer.assigned_paper.select_related('assign_paper')