from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ad(models.Model):
    CONDITION_CHOICES = [('new', 'Новый'), ('used', 'Б/У')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=100)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.title} ({self.user.username})"

class ExchangeProposal(models.Model):
    STATUS_CHOICES = [('pending', 'Ожидает'), ('accepted', 'Принята'), ('declined', 'Отклонена')]
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_proposals')
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('ad_sender', 'ad_receiver')
    def __str__(self):
        return f"Proposal {self.id}: {self.ad_sender} -> {self.ad_receiver}"
