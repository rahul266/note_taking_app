from django.db import models
from .user import User

class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='owner_id')
    last_edited_by=models.ForeignKey(User, on_delete=models.CASCADE,related_name='last_editor_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'notes'