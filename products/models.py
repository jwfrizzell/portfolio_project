from django.db import models
from datetime import date

# Create your models here.
class Product(models.Model):
	title = models.CharField(max_length=30)
	url = models.CharField(max_length=500)
	pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
	votes_total = models.IntegerField()
	icon = models.ImageField(upload_to='images')
	image = models.ImageField(upload_to='images')
	body = models.TextField()


	def pub_date_pretty(self):
		return self.pub_date.strftime('%b %e %Y')

	def summary(self):
		return self.body[:100]

	def __str__(self):
		return self.title