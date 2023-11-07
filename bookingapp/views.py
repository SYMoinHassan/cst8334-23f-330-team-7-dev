from django.shortcuts import render, redirect
from .forms import WorkstationBookingForm, SignUpForm
from .models import Booking, Workstation, CustomUser
from django.contrib import messages

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.models import User, Group
from django.views import View

from .forms import CustomUserLoginForm
from django.contrib.auth import authenticate, login

from .forms import CreateLabForm
from .models import Laboratory


def index(request):
    return render(request, 'bookingapp/index.html', {'index': index})


class Register(CreateView):
    form_class = SignUpForm
    model = User
    success_url = reverse_lazy('index')
    template_name = 'bookingapp/register.html'


    def form_valid(self, form):
        # Check if the form is valid
        if form.is_valid():
            user = form.save()

            # Retrieve the 'Custom Users' group
            group = Group.objects.get(name='Custom Users')

            # Add the user to the 'Custom Users' group
            user.groups.add(group)

            # Extract email from the form and create a CustomUser instance
            email = form.cleaned_data.get('email')
            CustomUser.objects.create(user=user, email=email)

            # Message upon successful sign up
            messages.success(self.request, "Successfully signed up!")


            # Call the parent class's form_valid method
            return super().form_valid(form)

    
    def form_valid(self, form):
        # No need to check form.is_valid() here; it's already done before this method is called.
        user = form.save()

        # Add the user to a group if necessary
        group = Group.objects.get(name='Custom Users')
        user.groups.add(group)

        # No need to create a CustomUser again; `form.save()` already handled it.
        # Just make sure any additional logic (like sending confirmation emails) is covered.

        return super().form_valid(form)

class CustomLoginView(View):
    template_name = 'bookingapp/login.html'
    form_class = CustomUserLoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in!")  # Add this line for the message
                return redirect('index')  # Redirect to your desired URL after login
            else:
                # Handle invalid login
                messages.success(request, "Error logging in. Please check your credentials and try again.")  # Add this line for the message
                

        return render(request, self.template_name, {'form': form})
    
from django.contrib.auth import logout

def logout_view(request):
    logout(request)  # This will log out the user and invalidate their session.
    return redirect('index')  # Redirect to homepage (or any other view) after logout.

def user_list(request):
    users = User.objects.all()
    return render(request, 'bookingapp/user_list.html', {'users': users})

from django.contrib.auth.mixins import LoginRequiredMixin

class BookWorkstation(LoginRequiredMixin, View):
    login_url = '/bookingapp/login/'  # Replace with the URL of your login view

    
    def get(self, request):
    # Get all available workstations
        available_workstations = Workstation.objects.filter(available=True)
        form = WorkstationBookingForm()
        return render(request, 'bookingapp/book_workstation.html', {'form': form, 'available_workstations': available_workstations})

    def post(self, request):
        if request.method == 'POST':
            form = WorkstationBookingForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                workstation_number = form.cleaned_data['workstation_number']
                date = form.cleaned_data['date']
                time = form.cleaned_data['time']

                # Check if a booking already exists for the specified workstation, date, and time
                existing_booking = Booking.objects.filter(
                    workstation__number=workstation_number,
                    date=date,
                    time=time
                )

                if existing_booking.exists():
                    # Display a message to the user
                    messages.error(request, 'Workstation already booked for the selected date and time.')
                else:
                    # Retrieve or create the Workstation instance based on the workstation_number
                    workstation, created = Workstation.objects.get_or_create(number=workstation_number)

                    # Check if the workstation is available
                    if workstation.available:
                        # Mark the workstation as unavailable
                        workstation.available = False
                        workstation.save()

                        # Create a new booking
                        Booking.objects.create(
                            user=username,
                            workstation=workstation,
                            number=workstation_number,
                            date=date,
                            time=time,
                            email=email
                        )

                        return redirect('booking_success')  # Replace 'booking_success' with your actual success URL
                    else:
                        # Display a message to the user that the workstation is not available
                        messages.error(request, 'Selected workstation is not available for the selected date and time.')

        else:
            form = WorkstationBookingForm()

        return render(request, 'bookingapp/book_workstation.html', {'form': form, 'available_workstations': available_workstations})

def booking_success(request):
    bookings = Booking.objects.all()

    return render(request, 'bookingapp/booking_success.html', {'bookings': bookings})

def display_bookings(request):
    # Retrieve all booking entries from the database
    bookings = Booking.objects.all()

    # Pass the bookings to the template
    return render(request, 'bookingapp/display_bookings.html', {'bookings': bookings})

def available_workstations(request):
     # Get all available workstations
    available_workstations = Workstation.objects.filter(available=True)

    return render(request, 'bookingapp/available_workstations.html', {'workstations': available_workstations})

def create_lab(request):
    if request.method == 'POST':
        form = CreateLabForm(request.POST)
        if form.is_valid():
            # Create a new Laboratory object from the form data, without availability_days
            lab = Laboratory.objects.create(
                lab_name=form.cleaned_data['lab_name'],
                lab_room_number=form.cleaned_data.get('lab_room_number', ''),
                number_of_workstations=form.cleaned_data['number_of_workstations'],
                description=form.cleaned_data.get('description', ''),
                availability_time=form.cleaned_data.get('availability_time', '')
            )
            
            # The redirect should go to the success page's actual name in your URL configuration
            return redirect('lab_creation_success')
    else:
        form = CreateLabForm()

    return render(request, 'bookingapp/create_lab.html', {'form': form})

def lab_creation_success(request):
    # ... implementation ...
    return render(request, 'bookingapp/lab_creation_success.html')


