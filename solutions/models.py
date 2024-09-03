from django.db import models


class Solution(models.Model):
    """
    Define the attributes of individual solutions
    """
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(max_length=1500, null=True, blank=True)
    tech_stack = models.TextField(max_length=1500, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

