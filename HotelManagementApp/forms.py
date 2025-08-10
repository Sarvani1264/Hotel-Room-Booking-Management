from django import forms
from django.forms import ModelForm
from .models import Register, Room, Contact, Booking


class Reg(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = Register
        fields = ['username', 'email', 'mobile', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile number'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if Register.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if Register.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("This mobile is already registered.")
        return mobile

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("confirm_password")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['sender_name', 'sender_mail', 'message']
        labels = {
            'sender_name': 'Your Name',
            'sender_mail': 'Your Email',
            'message': 'Your Message',
        }
        widgets = {
            'sender_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'sender_mail': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 4}),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['username', 'email', 'mobile']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}),
        }

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['profile_image']

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current Password'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['roomnum', 'name', 'description', 'price_per_day', 'image']
        labels = {
            'roomnum': 'Room Number',
        }
        widgets = {
            'roomnum': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Room Number'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Room Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Room Description', 'rows': 4}),
            'price_per_day': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price per Day'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer_name','num_guests', 'check_in', 'check_out', 'special_requests']
        labels = {
            'customer_name': 'Full name',
        }
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }

class AdminBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user','room','customer_name','num_guests', 'check_in', 'check_out', 'special_requests', 'total_price', 'payment_status','total_price','is_cancelled']
        labels = {
            'customer_name': 'Full name',
        }
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }
