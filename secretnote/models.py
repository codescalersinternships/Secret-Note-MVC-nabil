from django.db import models
# from django.contrib import admin
import uuid
from django.utils import timezone


class Note(models.Model):
    note_url = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    note_text = models.CharField(max_length=200)
    note_remvisit = models.BigIntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    
