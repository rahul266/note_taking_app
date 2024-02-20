from django.db import models
from .user import User
from .note import Note

class NoteVersion(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    editor = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table='note_versions'
