from django.db import models


class Contact(models.Model):
    """
      Contact model for users to contact the company
    """
    SUBJECT_CHOICES = [
        ('', 'Please select one'),
        ('API', 'API Integration'),
        ('CMS', 'CMS Integration'),
        ('eComm', 'eCommerce Web Design'),
        ('SEO', 'Site Optimization (SEO)'),
        ('webDev', 'Web Development'),
        ('webHost', 'Web Hosting'),
        ('Other', 'Other'),
    ]
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    subject = models.CharField(max_length=7, choices=SUBJECT_CHOICES, null=False, blank=False)
    message = models.TextField(max_length=500, null=False, blank=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # using f-strings







