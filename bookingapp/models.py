from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.utils.translation import gettext_lazy as _

# User model

class CustomUser(AbstractUser):

    ROLES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('staff', 'Staff')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLES)

    class Meta:
        app_label = 'bookingapp'

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='bookingapp_user_set',  # Change 'bookingapp' as needed
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='bookingapp_user_set',  # Change 'bookingapp' as needed
    )

# Workstation model

class Workstation(models.Model):
    number = models.PositiveIntegerField(unique=True, choices=[(i, i) for i in range(1, 33)])
    available = models.BooleanField(default=True)


class Booking(models.Model):
    user = models.CharField(max_length=100)  # Assuming the maximum length for a username is 100 characters
    workstation = models.ForeignKey(Workstation, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(unique=False, choices=[(i, i) for i in range(1, 33)])    
    date = models.DateField()
    time = models.TimeField()
    email = models.EmailField(default='')  # Provide a default value

    def __str__(self):
        return f'{self.user} booked {self.workstation} on {self.date} at {self.time}'
    

class Laboratory(models.Model):
    lab_name = models.CharField(max_length=100)
    lab_room_number = models.CharField(max_length=10)
    number_of_workstations = models.IntegerField()
    description = models.TextField(blank=True)
    # Removed ArrayField and replaced with a related model 'AvailabilityDay'
    availability_time = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.lab_name

# Separate model to store availability days
class AvailabilityDay(models.Model):
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name='availability_days')
    day = models.CharField(max_length=10)

    def __str__(self):
        return self.day