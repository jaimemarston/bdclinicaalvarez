from django.db import models

from django.utils import timezone
import unicodedata

class Citas(models.Model):
    codigo = models.IntegerField(default=0)
    descripcion = models.CharField(max_length=30, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    objects = models.Manager()



class Usuarios(models.Model):
    username = models.CharField(max_length=200, null=True, blank=True)
    nombre = models.CharField(max_length=200, null=True, blank=True)
    apellido_paterno = models.CharField(max_length=200, null=True, blank=True)
    apellido_materno = models.CharField(max_length=200, null=True, blank=True)
    foto = models.ImageField(upload_to='usuarios', null=True, blank=True)
    sexo = models.IntegerField(null=True)
    correo = models.CharField(max_length=200, null=True, blank=True)
    telefono1 = models.CharField(max_length=50, null=True, blank=True)
    telefono2 = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    cargo = models.CharField(max_length=100, null=True, blank=True)
    dni = models.CharField(max_length=20, null=True, blank=True)

    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'

    _password = None


    def get_username(self):
        """Return the identifying username for this User"""
        return getattr(self, self.USERNAME_FIELD)

    def __init__(self, *args, **kwargs):
        super(Usuarios, self).__init__(*args, **kwargs)
        # Stores the raw password if set_password() is called so that it can
        # be passed to password_changed() after the model is saved.
        self._password = None

    def __str__(self):
        return self.get_username()

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def natural_key(self):
        return (self.get_username(),)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return 'email'

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username

    # def __str__(self):
    #     return self.nombre
