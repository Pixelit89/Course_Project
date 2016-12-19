from django.db import models
from personal_page.models import Account

class Chat(models.Model):
    created = models.DateTimeField(auto_now=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    companion_id = models.IntegerField()

    def __unicode__(self):
        return self.message
