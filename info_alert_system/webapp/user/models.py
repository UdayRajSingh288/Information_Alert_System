from django.db import models

class User(models.Model):
	email = models.EmailField(max_length = 160, unique = True)
	pswd_hash = models.BinaryField()

	def __str__(self):
		return self.email

class Alert(models.Model):
	topic = models.CharField(max_length = 50)
	search_phrase = models.CharField(max_length = 200)
	freq = models.IntegerField()
	last_mail = models.DateField()
	next_mail = models.DateField()
	user = models.ForeignKey(User, on_delete = models.CASCADE)

	def __str__(self):
		return self.search_phrase