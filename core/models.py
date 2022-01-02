from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

STATUS_CHOICES=[
	('Submitted','Submitted'),
	('Approved','Approved'),
	('Reject','Reject'),
]

class Author(models.Model):
	user = models.OneToOneField(User,related_name='author',on_delete=models.CASCADE)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_on']
		
	def __str__(self):
		return self.user.full_name


class Paper(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
	status = models.CharField(max_length=30,default='Submitted')
	file = models.FileField(upload_to='author_files/') # taking files from author
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	remarks = models.CharField(max_length=255,default='No-Remark')
	rating = models.IntegerField(default=0)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(null=True)
	review_by = models.IntegerField(default=0)
	is_review_submit = models.BooleanField(default=False)

	class Meta:
		ordering = ['-created_on']
		
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
	assign_paper = models.OneToOneField(Paper,related_name='paper_assign',on_delete=models.CASCADE)
	is_review = models.BooleanField(default=False)


	class Meta:
		ordering = ['-created_on']

	def __str__(self):
		return str(self.id)
# request.user.reviewer.assigned_paper.select_related('assign_paper')
#return f'{self.review.user.full_name} - {self.assign_paper.title}'


class Contact(models.Model):
	email = models.EmailField()
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	description = models.CharField(max_length=200)
	reply=models.CharField(max_length=255)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_on']

		def __str__(self):
			return self.email