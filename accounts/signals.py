from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import userProfile,User


#post_Save signals for receiver
@receiver(post_save,sender=User)
def create_profile_receiver(sender,instance,created,**kwargs):
    print(created)
    if created:
        userProfile.objects.create(user=instance) 
     
        print("userprofile created")
    else:
        try:
            profile=userProfile.objects.get(user=instance)
            profile.save()
        except:
            userProfile.objects.create(user=instance) 
            # we got the profile now

# pre_Save signals
@receiver(pre_save,sender=User)
def pre_save_profile(sender,instance,**kwargs):
    pass    
    # print(instance.username,"this is being saved")


