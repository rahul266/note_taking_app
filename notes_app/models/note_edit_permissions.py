from django.db import models
from .user import User
from .note import Note

class NoteEditPermissionsTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    class Meta:
        db_table='note_edit_permissions'
