# from django.core.exceptions import ValidationError
# import os

# def allow_image_only(value):
#     ext=os.path.splitext(value.name)[1] ;# cover-image.jpg  means 0->cover-image and 1->jpg 
#     print(ext)
#     valid_extensions =['.png','.jpg','.jpeg']
#     if not ext.lower in valid_extensions:
#         raise ValidationError("Unsupported file extensions .Allowed extensions: "+str(valid_extensions))


from django.core.exceptions import ValidationError
import os


def allow_only_images_validator(value):
    ext = os.path.splitext(value.name)[1] # cover-image.jpg
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Allowed extensions: ' +str(valid_extensions))
    
# so here str(valid...) means we concate the valid extension in message b