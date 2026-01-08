from src.core.models.base import *


class CourseModel(BaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey("CategoryModel", on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    price = models.DecimalField(max_digits=12, decimal_places=0)
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    level = models.CharField(max_length=50, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

