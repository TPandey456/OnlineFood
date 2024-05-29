from django.db import models
# from django.db.models.fields.related import ForeignKey,OneToOneField
from accounts.models import User,userProfile
from  accounts.utils import send_notification

class Vendor(models.Model):
    user=models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile= models.OneToOneField(userProfile, related_name='userprofile',on_delete=models.CASCADE)
    vendor_name=models.CharField(max_length=50)
    vendor_license=models.ImageField(upload_to='vendor/license')
    is_approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.vendor_name
    
    def save(self,*args,**kwargs):
# if we dont now how many parameter this pariticular save function accepts
        if self.pk is not None:
            # update
            orignal= Vendor.objects.get(pk=self.pk)
            if self.pk is not None:
                if orignal.is_approved != self.is_approved:
# here it means the original status and the status that we change  if both are not equal it means is_Approved status getting change
                    mail_template="accounts/emails/admin_approval_email.html"
                    context={
                            'user':self.user,
                            'is_approved':self.is_approved
                        } # because y same niche if else dono m use hrhe the islie 
                    if self.is_approved ==True:
                        mail_subject="Your restaurant request has been approved! "
# bcz in mailtemplate is a html file that y we use context
                        
                        send_notification(mail_subject,mail_template,context)
                    else:
                        mail_subject="Sorry! You are not eligible"
                       
                        send_notification(mail_subject,mail_template,context)
# dynamic way to sending the notification email
        return super(Vendor,self).save(*args,**kwargs)
# super function will actually allow you to access the save method of this particular class this is the syntax

    