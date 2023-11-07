from django.contrib import admin
from .models import Workstation  # Import your Workstation model
from .models import Laboratory 

# Register the Workstation model
admin.site.register(Workstation)
admin.site.register(Laboratory)