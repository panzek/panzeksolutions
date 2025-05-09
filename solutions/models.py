from django.db import models
from django_resized import ResizedImageField
from django_ckeditor_5.fields import CKEditor5Field

from django.utils.html import strip_tags
from django.utils.text import Truncator


class Solution(models.Model):
    """
    Define the attributes of individual solutions
    """
    name = models.CharField(max_length=200, null=False, blank=False)
    description = CKEditor5Field('Description', config_name='default', null=True, blank=True)
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
    
    def get_truncated_description(self, word_limit=42):

        # Strip HTML tags from description
        clean_text = strip_tags(self.description)
        # Truncate to specified number of words
        truncated_text = Truncator(clean_text).words(word_limit, html=False)
        return truncated_text

    def __str__(self):
        return self.name

