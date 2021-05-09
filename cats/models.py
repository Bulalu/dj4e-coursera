from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.
class Breed(models.Model):
    name = models.CharField(
            max_length = 200,
            validators=[MinLengthValidator(2,'Breed must greater than two characters')]
    )

    def __str__(self):
        return self.name


class Cat(models.Model):
    nickname = models.CharField(
            max_length = 200,
            validators=[MinLengthValidator(2,'Nickname must greater than two characters')]
    )

    breed = models.ForeignKey('Breed', on_delete=models.CASCADE, null=False)
    foods = models.CharField(max_length=300)
    weight = models.PositiveIntegerField()
    

    def __str__(self):
        return self.nickname
        