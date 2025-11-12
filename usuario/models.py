from django.db import models
from django.conf import settings

class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth=models.DateField(blank=True, null=True) #blank es para validaciones, null es para la base de datos

    def __str__(self):
        return f'Perfil de {self.user.username}'
    
