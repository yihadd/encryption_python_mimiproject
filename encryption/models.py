from django.db import models

class EncryptedText(models.Model):
    plain_text = models.TextField()
    cipher_text = models.TextField()
    encryption_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.encryption_type} - {self.created_at}"
