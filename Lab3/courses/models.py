from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'categories'  # Ca să nu scrie Django "Categorys" în admin

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    year = models.IntegerField()
    semester = models.CharField(
        max_length=10,
        choices=[('fall', 'Fall'), ('spring', 'Spring')],
        default='fall',
    )
    # Relație: un curs aparține de o categorie. Dacă ștergi categoria, se șterg și cursurile (CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='courses',
    )
    # Exercițiul A: Am adăugat direct câmpul de credite cu o valoare default (4)
    credits = models.IntegerField(default=4)

    def __str__(self):
        return f"{self.title} ({self.year})"