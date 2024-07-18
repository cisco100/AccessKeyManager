from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import get_user_model
 
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    school_name=forms.CharField(
        widget=forms.TextInput(
            attrs={
            "placeholder":"schoool name",
            "class":"form-control",
            }))
    
    email=forms.EmailField(
        widget=forms.EmailInput(
            attrs={
            "placeholder":"school email",
            "class":"form-control"
            }))


    personnel_name=forms.CharField(
        widget=forms.TextInput(
            attrs={
            "placeholder":"IT-Personnel name",
            "class":"form-control",
            }))
     


    password1=forms.CharField(
        widget=forms.PasswordInput(
            attrs={
            "placeholder":"password",
            "class":"form-control",
            }))

    password2=forms.CharField(
        widget=forms.PasswordInput(
            attrs={
            "placeholder":"Re-enter password",
            "class":"form-control",
            }))


    class Meta:
        model = User
        fields = ("school_name","email","personnel_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_active = False  # User won't be active until email is verified
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    
    
    email=forms.EmailField(
        widget=forms.EmailInput(
            attrs={
            "placeholder":"email",
            "class":"form-control"
            }))


    password=forms.CharField(
        widget=forms.PasswordInput(
            attrs={
            "placeholder":"password",
            "class":"form-control",
            }))



class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("There is no active user associated with this email address")
        return email