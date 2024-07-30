from django.db import models


class Contact(models.Model):
    """
    Contact model for site visitors to contact us
    """

    firstName = models.CharField(max_length=100, null=False, blank=False)
    lastName = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    subject = models.CharField(max_length=200, null=False, blank=False)
    message = models.TextField(max_length=500, null=False, blank=False)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"  # using f-strings
