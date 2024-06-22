from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage   
from django.contrib import messages
from django.conf import settings
def detectUser(user):  
    if user.role == 1:
        redirectUrl= "vendorDashboard"
        return redirectUrl
    elif user.role == 2:
        redirectUrl ="customerDashboard"
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl
      
def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()




def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    if(isinstance(context['to_email'], str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.content_subtype = "html"
    mail.send()

""" 
why we use if else condtion? 

so if we look at this view() ,  stored by we were atually sending email adress with to email key
which is already a list so while sending a order confirmation email we are sending the email to only one 
only single email adsress so this is now the string type inside the order> view.py  line 119('to_email': order.email)

so the utils.py was sending emails to the list , so that's y we checking if the email address is single 
that means if the email address is str type, then we wanted to put it into a list pass to parameter in line 45 utils.py
if the context is not str then list part is working line 44

 
 """