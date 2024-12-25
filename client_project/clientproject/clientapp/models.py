from django.db import models

# Create your models here.
class ImagePaths(models.Model):
    class ClassChoices(models.IntegerChoices):
        cancercell = (1,"cancercell")
        normalcell = (0,'normalcell')
    image_path = models.CharField(max_length=100)
    X = models.PositiveIntegerField()
    Y = models.PositiveIntegerField()
    patient_id = models.IntegerField(default=-1)
    classification = models.IntegerField(choices=ClassChoices.choices)
    def __str__(self):
        return f'{self.image_path}, {self.image_path}, {self.classification}'