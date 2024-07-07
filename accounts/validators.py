from django.core.exceptions import ValidationError
import os

def allow_only_images_validators(value):
    ext = os.path.splitext(value.name)[1]
    print(ext)
    valid_extention =['.png', '.jpg', '.jpeg']
    if not ext.lower() in valid_extention:
        raise ValidationError('Unsupported file extention. Allow extention : ' + str(valid_extention))