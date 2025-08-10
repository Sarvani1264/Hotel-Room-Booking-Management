from django.db import models
from django.utils import timezone

# Create your models here.
class Register(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, unique=True, blank=True)
    password = models.TextField(max_length=100)
    joined_date = models.DateField(default=timezone.now)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.username

class Admin(models.Model):
    username = models.CharField(max_length=100, unique=True)
    admin_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    joined_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.admin_id})"

class Room(models.Model):
    roomnum = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)

    def __str__(self):
        return self.roomnum

    def availability_status(self):
        today = timezone.now().date()
        booking = self.booking_set.filter(
            is_cancelled="active",
            check_out__gte=today
        ).order_by('check_in').first()

        if booking:
            if booking.check_in <= today <= booking.check_out:
                return f"Not available from {booking.check_in} to {booking.check_out}"
            else:
                return f"Available upto {booking.check_in} and after {booking.check_out}"

        return "Available now"

class Contact(models.Model):
    sender_name = models.CharField(max_length=100)
    sender_mail = models.EmailField()              
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sn} - {self.sm}"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
    )
    PAYMENT_CHOICES = (
        ('pending', 'Pending'),
        ('payment done', 'Payment Done'),
    )
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    num_guests = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=100)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price=models.PositiveIntegerField()
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES,default='Pending')
    is_cancelled = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    special_requests = models.TextField(blank=True, null=True)
    booked_on = models.DateTimeField(auto_now_add=True)

    def total_days(self):
        return (self.check_out - self.check_in).days

    def cal_total_price(self):
        return self.total_days() * self.room.price