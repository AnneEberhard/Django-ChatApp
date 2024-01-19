from django.db import models
from django.db.models.fields import DateField
from datetime import date
from django.conf import settings

class Message(models.Model):
    text = models.CharField(max_length=500)
    created_at = DateField(default=date.today)
    # chat = Chat Klasse verknüpfen
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set')
        # foreignkey referenziert auf ein anderes Objekt
        # on_delete=models.CASCADE sorgt dafür, dass wenn der Nutzer gelöscht wird, die Nachricht auch gelöscht wird
        # related_name='author_message_set' info für die Datenbank: es geht um author im model message
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_message_set')