from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode 
from django.contrib.auth.models import User
from . forms import CreateUserForm
from . token import user_tokenizer_generate

# Create your views here.
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.is_active = False # after registering the user, it is not active yet.
            user.save()

            # email verification
            current_site = get_current_site(request)
            subject = 'Account verification email'
            
            message = render_to_string('account/registration/email-verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user)
            })

            user.email_user(subject=subject, message=message)
            
            print('email sent')
            return redirect('email-verification-sent')

    return render(request, 'account/registration/register.html', {'form': form})


def email_verification(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    # if success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')

    # if failed
    else:
        return redirect('email-verification-failed')
    
def email_verification_success(request):
    return render(request, 'account/registration/email-verification-success.html')

def email_verification_faied(request):
    return render(request, 'account/registration/email-verification-failed.html')

def email_verification_sent(request):
    return render(request, 'account/registration/email-verification-sent.html')