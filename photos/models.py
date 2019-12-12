# from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone
# Create your models here.

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Photo(models.Model):
	image = models.ImageField(upload_to='uploads/')
	caption = models.TextField()
	updated_at = models.DateTimeField(auto_now_add=True)
	published_at = models.DateTimeField(null=True)
	status = models.IntegerField(choices=STATUS, default=0)
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	class Meta:
		ordering=['-published_at']

	def publish(self):
		self.published_at = timezone.now()
		self.save()

	def __str__(self):
		return self.caption

