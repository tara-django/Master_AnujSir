from django.shortcuts import render, HttpResponse
from django.views import View
from accounts.forms import UserRegistrationForm

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.core.mail import EmailMessage
from accounts.tokens import activation_token

from accounts.models import User


# Create your views here.


class UserRegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = UserRegistrationForm()
        template_name = "accounts/signup.html"
        return render(request, template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            message_subject = "Activate your account"
            domain_url = get_current_site(request)
            user_email = form.cleaned_data["email"]
            message = render_to_string(
                "accounts/activation_message.html",
                {
                    "domain": domain_url.domain,
                    "user": user,
                    "uid": urlsafe_base64_encode(force_bytes(user.id)),
                    "token": activation_token.make_token(user),
                },
            )

            email = EmailMessage(message_subject, message, to=[user_email])
            email.send()
            activation_msg = "Open your email to activate account."
            return render(
                request, "accounts/activate_email.html", {"activation_msg": activation_msg}
            )

        template_name = "accounts/signup.html"
        return render(request, template_name, {"form": form})


def activate(request, uidb64, token):
    print("I am active view")
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except (ValueError, User.DoesNotExist):
        user = None

    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        return render(request, "accounts/activation_success.html")
    return render(request, "accounts/activation_fail.html")
