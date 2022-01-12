from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 討論主題
class Topic(models.Model):
    subject = models.CharField('討論主題', max_length=255)
    content = models.TextField('內文')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField('建立時間', auto_now_add=True)
    replied = models.DateTimeField('回覆時間', null=True, blank=True)
    hits = models.IntegerField('瀏覽次數', default=0)

    def __str__(self):
        return "{}: {}".format(self.author, self.subject)
# 討論主題內的回覆
class Reply(models.Model):
    topic = models.ForeignKey(Topic, models.CASCADE)
    content = models.TextField('回覆內容')
    author = models.ForeignKey(User, models.CASCADE)
    created = models.DateTimeField('回覆時間', auto_now_add=True)

    def __str__(self):
        return "{} | {}: {}".format(
            self.topic, 
            self.author, 
            self.content
        )