from django.db import models

# Create your models here.

class Participant(models.Model):
	name=models.CharField(max_length=200,null=True,blank=True)
	email = models.CharField(max_length=200, null=True)
	resume = models.FileField(upload_to="resume",blank = True)
	def __str__(self):
		return self.name



class Interview(models.Model):
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	participants=models.ManyToManyField(Participant)
	
	def __str__(self):
		return str(self.id)
