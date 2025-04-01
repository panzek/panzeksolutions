from django.db import models
from django_resized import ResizedImageField


class Solution(models.Model):
    """
    Define the attributes of individual solutions
    """
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    tech_stack = models.TextField(null=True, blank=True)
    image = ResizedImageField(
        size=[800, 400],
        crop=['middle', 'center'],
        quality=75,
        upload_to='solutions_image/',
        force_format='WEBP',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

