from django.db import models

class Article(models.Model):
    CATEGORY_CHOICES = [
        ('Crop Management', 'Crop Management'),
        ('Soil Health', 'Soil Health'),
        ('Organic Farming', 'Organic Farming'),
        ('Pest Management', 'Pest Management'),
        ('Irrigation', 'Irrigation'),
        ('Fertilizers', 'Fertilizers'),
        ('Government Schemes', 'Government Schemes'),
        ('Weather', 'Weather'),
        ('Modern Farming', 'Modern Farming'),
    ]

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Crop Management')
    summary = models.TextField(help_text="Concise overview for cards")
    content = models.TextField(help_text="Complete article text / guide")
    official_source_url = models.URLField(max_length=500, blank=True, help_text="Link to official government or ICAR bulletin")
    read_time_minutes = models.IntegerField(default=4)
    is_government_scheme = models.BooleanField(default=False)
    image_url = models.URLField(max_length=500, blank=True)
    published_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return f"{self.title} ({self.category})"

class GovernmentResource(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, default='Government Portal')
    official_url = models.URLField(max_length=500)
    ministry_department = models.CharField(max_length=255, default='Ministry of Agriculture & Farmers Welfare')
    helpline = models.CharField(max_length=100, blank=True, default='1800-180-1551')
    description = models.TextField()
    beneficiary_criteria = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

