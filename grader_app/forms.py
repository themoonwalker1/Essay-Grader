from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, Essay

dropdown = (("None","None"),("APA","APA"),("MLA","MLA"))

class EssayForm(forms.Form):
    teacher = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Teacher's Ion Email"
        })
    )
    assignment = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex: Romeo and Juliet"
        })
    )
    title = forms.CharField(
        max_length=500, 
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Title"
        })
    )
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Write your essay here!"
        })
    )
    citation_type = forms.ChoiceField(choices=dropdown, required=True)

class LoginForm(forms.Form):
    email = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), max_length=150, required=True)
    
class SetupForm(forms.Form):
    first_name = forms.CharField(max_length=150, required=True)
    middle_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=True)
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    GRADUATE = 'GR'
    YEAR_IN_SCHOOL_CHOICES = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
        (GRADUATE, 'Graduate'),
    ]
    year_in_school = forms.ChoiceField(
        choices=YEAR_IN_SCHOOL_CHOICES,
    )

class ChangeForm(forms.Form):
    password_1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), max_length=150, required=True)
    password_2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), max_length=150, required=True)
    def disable(self):
        self.fields['password_1'].disabled = True
        self.fields['password_2'].disabled = True

class InfoForm(forms.Form):
    email = forms.EmailField(max_length=250, widget=forms.TextInput(attrs={'readonly':'readonly', "class": "form-control"}))
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    middle_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    
    def disable(self):
        self.fields['first_name'].disabled = True
        self.fields['middle_name'].disabled = True
        self.fields['last_name'].disabled = True

class TeacherForm(forms.Form): 
    period_1_teacher = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    period_2_teacher = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    period_3_teacher = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    period_4_teacher = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    period_5_teacher = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    period_6_teacher = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    period_7_teacher = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control"}), required=False)
    
    def clean_teacher(self, period):
        name = period + " Period Teacher"
        teacher = self.cleaned_data.get(name)
        if teacher:
            raise forms.ValidationError
        return teacher
    
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'admin')

    def clean_password(self):
        return self.initial["password"]
