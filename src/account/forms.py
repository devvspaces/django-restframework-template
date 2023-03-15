from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, Profile
from utils.base.validators import validate_special_char


# User form for admin
class UserRegisterForm(forms.ModelForm):
	password=forms.CharField(label="Password",
							widget=forms.PasswordInput,
							min_length=8,
							help_text=password_validation.password_validators_help_text_html())
	password2=forms.CharField(label="Confirm password",
							widget=forms.PasswordInput,
							help_text='Must be similar to first password to pass verification')
	
	username = forms.CharField(max_length=20, label='Profile Username', help_text='Enter a unique username for this user', required=False)
	account_type = forms.ChoiceField(choices=Profile.ACCOUNT_TYPES, required=False)

	class Meta:
		model=User
		fields=("email","username","password","password2",)
	
	# Validate the username if unique
	def clean_username(self):
		username = self.cleaned_data.get("username")

		# Validate the username has only valid chars
		validate_special_char(username)
		
		# Does username already exist
		if Profile.objects.filter(username__exact=username).exists():
			raise forms.ValidationError('Username name is not available')

		return username

	# Cleaning password one to check if all validations are met
	def clean_password(self):
		ps1=self.cleaned_data.get("password")
		password_validation.validate_password(ps1,None)
		return ps1

	"""Override clean on password2 level to compare similarities of password"""
	def clean_password2(self):
		ps1=self.cleaned_data.get("password")
		ps2=self.cleaned_data.get("password2")
		if (ps1 and ps2) and (ps1 != ps2):
			raise forms.ValidationError("The passwords does not match")
		return ps2
		
	""" Override the default save method to use set_password method to convert text to hashed """
	def save(self, commit=True):
		user=super(UserRegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data.get("password"))

		if commit:
			user.save()

			# Profile is already created, update values with data in form
			profile = user.profile
			username = self.cleaned_data.get('username')
			account_type = self.cleaned_data.get('account_type')

			# Add data
			profile.username = username if username else ''
			profile.account_type = account_type if account_type else ''
			profile.save()

		return user