from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Register, Admin, Room, Contact, Booking
from .forms import Reg, RoomForm, BookingForm, AdminBookingForm
from .forms import EditProfileForm, ProfileImageForm, ChangePasswordForm, ContactForm
from django.contrib.auth import logout as django_logout
from django.db import IntegrityError
from django.conf import settings
from django.core.mail import send_mail
from datetime import date


# Create your views here.
def login(request):
    form = Reg()
    cform = ContactForm()
    error = ''

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'login':
            uname = request.POST.get('uname')
            pwd = request.POST.get('pwd')
            try:
                user = Register.objects.get(username=uname)
                if pwd==user.password:
                    request.session['username'] = uname
                    request.session['user_id'] = user.user_id
                    return redirect('rooms')
                else:
                    error = 'Incorrect password'
            except Register.DoesNotExist:
                error = 'User not found'

        elif form_type == 'register':
            if request.method=="POST":
                try:
                    na=request.POST['username']
                    mb=request.POST['mobile']
                    em=request.POST['email']
                    pwd=request.POST['password']
                    Register.objects.create(username=na,mobile=mb,email=em,password=pwd)
                    return redirect('login')
                except IntegrityError:
                    error = 'Email is already registered.'
    return render(request, 'LogInPage.html', {'form': form, 'cform':cform, 'error': error})

def adminlogin(request):
    form = Reg()
    error =''
    if request.method == 'POST':
        uname = request.POST.get('adminUname')
        id = request.POST.get('adminId')
        pwd = request.POST.get('adminPwd')
        try:
            admin = Admin.objects.get(admin_id=id)
            if pwd==admin.password and admin.username == uname:
                request.session['username'] = uname
                return redirect('adminboard')
            else:
                error = 'Incorrect credentials'
        except Register.DoesNotExist:
            error = 'Admin not found'

    return render(request, 'adminLogin.html', {'form': form, 'error': error})

def mail(request):
    form = Reg()
    cform = ContactForm()
    msg = ''
    if request.method=="POST" and request.POST.get("form_type") == "contact":
        if cform.is_valid:
            sndr=request.POST['sender_name']
            sndrmail=request.POST['sender_mail']
            m=request.POST['message']
            Contact.objects.create(sender_name=sndr,sender_mail=sndrmail,message=m)
            subject = f"New Contact Message from {sndr}"
            message = f"Name: {sndr}\nEmail: {sndrmail}\n\nMessage:\n{m}"
            t = settings.EMAIL_HOST_USER
            rcr = [settings.EMAIL_HOST_USER]
            res = send_mail(subject, message, t, rcr)
            if res == 1:
                msg = "Mail Sent"
            else:
                msg = "Not Sent"
        else:
            return cform

    return render(request, 'LogInPage.html', {
        'form':form,
        'cform': cform,
        'msg': msg,
        'scroll': True
    })
 

def rooms(request):
    rooms = Room.objects.all()
    return render(request,'Rooms.html',{'rooms': rooms})

def profile(request):
    user = Register.objects.get(username=request.session['username'])
    edit_form = EditProfileForm(instance=user)
    image_form = ProfileImageForm(instance=user)
    password_form = ChangePasswordForm()
    return render(request, 'profile.html', {
        'user': user,
        'edit_form': edit_form,
        'image_form': image_form,
        'password_form': password_form,
        'error': ''
    })

def edit_profile(request):
    user = Register.objects.get(username=request.session['username'])
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
    return redirect('profile')


def edit_profile_image(request):
    user = Register.objects.get(username=request.session['username'])
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
    return redirect('profile')


def change_password(request):
    user = Register.objects.get(username=request.session['username'])
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        current = request.POST.get('current_password')
        new = request.POST.get('new_password')
        confirm = request.POST.get('confirm_password')
        if form.is_valid():
            if current==user.password:
                if new == confirm:
                    user.password = new
                    user.save()
                else:
                    return render(request, 'profile.html', {
                        'user': user,
                        'edit_form': EditProfileForm(instance=user),
                        'image_form': ProfileImageForm(instance=user),
                        'password_form': form,
                        'error': 'New passwords do not match.'
                    })
            else:
                return render(request, 'profile.html', {
                    'user': user,
                    'edit_form': EditProfileForm(instance=user),
                    'image_form': ProfileImageForm(instance=user),
                    'password_form': form,
                    'error': 'Current password is incorrect.'
                })
    return redirect('profile')

def logout(request):
    django_logout(request)
    return redirect('login')

def adminboard(request):
    rooms = Room.objects.all()
    total_rooms = rooms.count()

    room_types = rooms.values('name').distinct().count()

    min_price = rooms.order_by('price_per_day').first()
    max_price = rooms.order_by('-price_per_day').first()

    context = {
        'total_rooms': total_rooms,
        'room_types': room_types,
        'min_price': min_price.price_per_day if min_price else 0,
        'max_price': max_price.price_per_day if max_price else 0,
    }
    return render(request,'adminaccess.html',context)

def manage_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'manageRooms.html', {'rooms': rooms})

def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_rooms')
    else:
        form = RoomForm()
    return render(request, 'addEditRooms.html', {'form': form})

def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            return redirect('manage_rooms')
    else:
        form = RoomForm(instance=room)
    return render(request, 'addEditRooms.html', {'form': form, 'room': room})

def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    room.delete()
    return redirect('manage_rooms')

def booking(request, room_id):
    room = Room.objects.get(roomnum=room_id)
    user_id = request.session.get('user_id') 
    profile = get_object_or_404(Register, user_id=user_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = profile
            booking.total_price = booking.total_days() * room.price_per_day
            booking.save()
            return render(request, 'booking_confirmation.html', {
                'booking': booking,
                'email': profile.email,
                'phone': profile.mobile
            })
    else:
        form = BookingForm()

    return render(request, 'BookingsPage.html', {
        'room': room,
        'form': form,
        'email': profile.email,
        'phone': profile.mobile
    })
    return render(request, 'BookingsPage.html',{'room':room})

def my_bookings(request):
    user = Register.objects.get(username=request.session['username'])
    bookings = Booking.objects.filter(user=user).order_by('-check_in')
    today = date.today()
    return render(request, 'my_bookings.html', {'bookings': bookings, 'today': today})


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    if booking.check_out >= date.today():
        booking.is_cancelled = 'cancelled'
        booking.save()
    return redirect('my_bookings')

def manage_bookings(request):
    bookings= Booking.objects.all()
    return render(request, "Admin_bookingaccess.html",{'bookings':bookings})

def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    if request.method == 'POST':
        form = AdminBookingForm(request.POST, request.FILES, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('manage_bookings')
        else:
             print(form.errors)
    else:
        form = AdminBookingForm(instance=booking)
    return render(request, 'AddEditBookings.html', {'form': form, 'booking': booking})

def add_booking(request):
    if request.method == 'POST':
        form = AdminBookingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_bookings')
    else:
        form = AdminBookingForm()
    return render(request, 'AddEditBookings.html', {'form': form})