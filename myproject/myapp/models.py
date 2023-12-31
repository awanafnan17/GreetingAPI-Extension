from django.db import models

class Greeting(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.message