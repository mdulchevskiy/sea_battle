import re
from django import forms
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from sea_battle.models import User


class UploadForm(forms.Form):
    upload = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'image_field',
            'id': 'image_field', }),
        error_messages={
            'invalid_image': 'The chosen file is not a valid image file.',
            'invalid': 'The chosen file is not a valid image file.', },
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data:
            file = cleaned_data['upload']
            if file:
                if file.size <= settings.MAX_FILE_SIZE:
                    if file.image.width != file.image.height:
                        raise forms.ValidationError('Image should be at least N×Npx (square).')
                else:
                    raise forms.ValidationError(
                        f'File size should be less than {filesizeformat(settings.MAX_FILE_SIZE)} '
                        f'(current: {filesizeformat(file.size)}).')
            else:
                raise forms.ValidationError('No file chosen.')
            return cleaned_data


class UserInfoForm(forms.Form):
    @classmethod
    def class_name(cls):
        return cls.__name__

    first_name = forms.CharField(
        label='First name',
        max_length=255,
        error_messages={'required': 'Required field'},
        widget=forms.TextInput(attrs={
            'size': 25,
            'class': 'edit_profile_form', }),
    )
    last_name = forms.CharField(
        label='Last name',
        max_length=255,
        error_messages={'required': 'Required field'},
        widget=forms.TextInput(attrs={
            'size': 25,
            'class': 'edit_profile_form', }),
    )
    email = forms.EmailField(
        error_messages={
            'required': 'Required field',
            'invalid': 'Not valid field', },
        widget=forms.TextInput(attrs={
            'size': 30,
            'class': 'edit_profile_form', }),
    )
    phone_number = forms.CharField(
        max_length=17,
        error_messages={'required': 'Required field'},
        widget=forms.TextInput(attrs={
            'size': 20,
            'class': 'edit_profile_form', }),
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        patterns = settings.PHONE_NUMBER_PATTERNS
        for pattern in patterns:
            match = re.fullmatch(pattern, phone_number)
            if match:
                break
        else:
            message_1 = 'Not valid field'
            message_2 = 'Enter a valid phone number'
            message = message_1 if self.class_name() == 'UserInfoForm' else message_2
            raise forms.ValidationError(message)
        return phone_number

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            message_1 = 'Not valid field'
            message_2 = 'Enter a valid first name'
            message = message_1 if self.class_name() == 'UserInfoForm' else message_2
            raise forms.ValidationError(message)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            message_1 = 'Not valid field'
            message_2 = 'Enter a valid last name'
            message = message_1 if self.class_name() == 'UserInfoForm' else message_2
            raise forms.ValidationError(message)
        return last_name

    def as_myp(self):
        return self._html_output(
            normal_row=f'<p style="margin-top: 5px; margin-bottom: 5px;">%(label)s %(field)s %(help_text)s</p>',
            error_row='<span style="color: red;">%s</span>',
            row_ender='',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        error_messages={'required': 'Username is required'},
        widget=forms.TextInput(attrs={'size': 28}),
    )
    password = forms.CharField(
        max_length=255,
        error_messages={'required': 'Password is required'},
        widget=forms.PasswordInput(attrs={'size': 28}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError('User with that username was not found!')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        username = cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if user and password and user.password != password:
            self.add_error('password', 'Incorrect password')
        return cleaned_data

    def as_myps(self):
        return self._html_output(
            normal_row=f'<p>%(label)s %(field)s %(help_text)s </p>',
            error_row='<span style="color: red;">%s</span>',
            row_ender='</p>',
            help_text_html=' <span class="helptext">%s</span>',
            errors_on_separate_row=True)


class PreRegForm(SignInForm):
    conf_password = forms.CharField(
        label='Confirm password',
        max_length=255,
        error_messages={'required': 'Password confirmation is required'},
        widget=forms.PasswordInput(attrs={'size': 28}),
    )


class RegForm(UserInfoForm, PreRegForm):
    first_name = forms.CharField(
        label='First name',
        max_length=255,
        error_messages={'required': 'First name is required'},
        widget=forms.TextInput(attrs={'size': 28}),
    )
    last_name = forms.CharField(
        label='Last name',
        max_length=255,
        error_messages={'required': 'Last name is required'},
        widget=forms.TextInput(attrs={'size': 28}),
    )
    email = forms.EmailField(
        error_messages={
            'required': 'Email is required',
            'invalid': 'Enter a valid email', },
        widget=forms.TextInput(attrs={'size': 28}),
    )
    phone_number = forms.CharField(
        max_length=17,
        error_messages={'required': 'Phone number is required'},
        widget=forms.TextInput(attrs={'size': 28}),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).first()
        check_1 = username.startswith('_') or username.startswith('.')
        check_2 = username.endswith('_') or username.endswith('.')
        check_3 = username.endswith('-') or username.endswith('-')
        check_4 = username.replace('_', '').replace('.', '').replace('-', '').isalnum()
        check = not check_1 and not check_2 and not check_3 and check_4
        if not check:
            raise forms.ValidationError('Enter a valid username')
        if user:
            raise forms.ValidationError('User with that username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).first()
        if user:
            raise forms.ValidationError('User with that email already exists')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        conf_password = cleaned_data.get('conf_password')
        if password:
            if not password.isalnum() or len(password) < 10:
                self.add_error('password', 'Incorrect format for password')
        if password and conf_password:
            if password != conf_password:
                self.add_error('conf_password', "Passwords don't match")
        return cleaned_data
