from django.db import models
from complaint.models import Complaint
from django.contrib.auth.models import User


class Comment(models.Model):
    """User comment"""
    complaint = models.ForeignKey(Complaint, related_name='comments',on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children',db_index=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null = True, on_delete=models.SET_NULL)
    user_comment = models.CharField(max_length=2000, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    # approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user_comment[:20]