import smtplib
from validate_email import validate_email
from django.conf import settings
from django.core.mail import send_mail
from django.core.files.storage import default_storage
from django.template import loader
from django.shortcuts import (redirect,
                              render, )
from sea_battle.forms import (UploadForm,
                              UserInfoForm, )
from sea_battle.models import User
from sea_battle.funcs import (check_connection,
                              get_session_key,
                              get_signed_user,
                              phone_number_formatting,
                              UserGameInfo, )


def account_page(request, username=None):
    session_key = get_session_key(request)
    request.session[f'referer_{session_key}'] = 'account_page'
    user_object = User.objects.filter(username=username)
    user = user_object.first()
    signed_user = get_signed_user(session_key).first()

    if request.method == 'GET':
        if user:
            user_game_info = UserGameInfo(user)
            editable_page_flag = signed_user and user_game_info.username == signed_user.username
            attr_dict = {
                'first_name': user_game_info.first_name,
                'last_name': user_game_info.last_name,
                'email': user_game_info.email,
                'phone_number': user_game_info.phone_number,
            }
            upload_form = UploadForm() if editable_page_flag else None
            user_info_form = UserInfoForm(initial=attr_dict) if editable_page_flag else None
            return render(request, 'profile_page.html', {
                'user_game_info': user_game_info,
                'upload_form': upload_form,
                'user_info_form': user_info_form,
                'editable_page_flag': editable_page_flag,
            })
        elif not username and signed_user:
            return redirect(f'/account/{signed_user.username}')
        elif not username and not signed_user:
            return redirect('sign_in')
        else:
            return render(request, '404.html')

    elif request.method == 'POST':
        user_game_info = UserGameInfo(user)
        editable_page_flag = user_game_info.username == signed_user.username
        attr_dict = {
            'first_name': user_game_info.first_name,
            'last_name': user_game_info.last_name,
            'email': user_game_info.email,
            'phone_number': user_game_info.phone_number,
        }
        user_info_form = UserInfoForm(initial=attr_dict)
        message = None
        invalid_field_flag = None
        save_info_flag = request.POST.get('save_info')
        upload_pic_flag = request.POST.get('upload_pic')
        remove_pic_flag = request.POST.get('remove_pic')
        send_email_flag = request.POST.get('send_mail')

        if send_email_flag:
            user_email = user_game_info.email
            if check_connection():
                if user_email:
                    if validate_email(user_email):
                        html_message = loader.render_to_string(
                            'email_message.html',
                            {'user_game_info': user_game_info}, )
                        try:
                            send_mail(
                                subject='Sea Battle',
                                message='',
                                html_message=html_message,
                                from_email=settings.EMAIL_HOST_USER,
                                recipient_list=[user_email],
                            )
                        except ConnectionError:
                            message = 'Something go wrong. Check your email settings.'
                        except smtplib.SMTPException:
                            message = 'Something go wrong. Check your email settings.'
                        else:
                            message = 'Your profile statistics has been send to your email.'
                    else:
                        message = "Cannot send email. User's email not valid."
                else:
                    message = 'Cannot send email. No email address in the profile.'
            else:
                message = 'Cannot send email. Check your internet connection.'

        if save_info_flag:
            form = UserInfoForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user_object.update(
                    first_name=data.get('first_name').capitalize(),
                    last_name=data.get('last_name').capitalize(),
                    email=data.get('email'),
                    phone_number=phone_number_formatting(data.get('phone_number')),
                )
                user = User.objects.filter(username=username).first()
                user_game_info = UserGameInfo(user)
                attr_dict = {
                    'first_name': user_game_info.first_name,
                    'last_name': user_game_info.last_name,
                    'email': user_game_info.email,
                    'phone_number': user_game_info.phone_number,
                }
                user_info_form = UserInfoForm(initial=attr_dict)
            else:
                user_info_form = UserInfoForm(request.POST)
                invalid_field_flag = True

        if upload_pic_flag:
            upload_form = UploadForm(request.POST, request.FILES)
            if upload_form.is_valid():
                file = upload_form.cleaned_data['upload']
                pic_extension = file.image.format.lower()
                pic_name = f'{user_game_info.username}.{pic_extension}'
                with default_storage.open(pic_name, 'wb+') as storage:
                    for chunk in file.chunks():
                        storage.write(chunk)
                User.objects.filter(username=user_game_info.username).update(
                    profile_pic=f'{pic_name}')
                return redirect('account_page')
            else:
                message = list(upload_form.errors.values())[0][0]

        if remove_pic_flag:
            if user_game_info.pic_exist:
                user.profile_pic.delete(save=False)
                User.objects.filter(username=user_game_info.username).update(profile_pic=None)
                return redirect('account_page')
            message = 'Cannot remove nonexistent picture.'

        return render(request, 'profile_page.html', {
            'user_game_info': user_game_info,
            'upload_form': UploadForm(),
            'user_info_form': user_info_form,
            'editable_page_flag': editable_page_flag,
            'invalid_field_flag': invalid_field_flag,
            'message': message, })
