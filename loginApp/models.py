from django.db import models
from datetime import date
import re

# Create your models here.
class UserManager(models.Manager):
    def regValidator(self, formInfo):
        today = date.today()
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        emailTaken = User.objects.filter(Email = formInfo['email'])



        if len(formInfo['fname']) == 0:
            errors['fnameReq'] = 'First Name is required!'
        elif len(formInfo['fname']) <2:
            errors['fnameLen'] = 'First Name should be at least 2 characters!'

        if len(formInfo['lname']) == 0:
            errors['lnameReq'] = 'Last Name is required!'
        elif len(formInfo['lname']) <2:
            errors['lnameLen'] = 'Last Name should be at least 2 characters!'

        if len(formInfo['email']) == 0:
            errors['emailReq'] = 'Email is required!'
        elif not EMAIL_REGEX.match(formInfo['email']):
            errors['emailMatch'] = 'Invaid email address!'
        elif len(emailTaken) > 0:
            errors['emailTaken'] = 'Email is taken'

        if len(formInfo['pword']) == 0:
            errors['pwReq'] = 'Password is required!'
        elif len(formInfo['pword']) < 8:
            errors['pwLen'] = 'Passwords should be at least 8 characters'

        if formInfo['pword'] != formInfo['pword2']:
            errors['pwMatch'] = 'Passwords must match!'
        
        if len(formInfo['bday']) == 0:
            errors['BdayReq'] = 'Birthday is required!'
        elif formInfo['bday'] > str(today):
            errors['bdayDate'] = "Birthday can't be in the future"



        return errors

    def loginValidator(self, formInfo):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(formInfo['emaillogin']) == 0:
            errors['emaillog'] = 'email needed to login!'
        elif not EMAIL_REGEX.match(formInfo['emaillogin']):
            errors['emailInval'] = 'Invaid email address!'
        if len(formInfo['pwlogin']) == 0:
            errors['pwneeded'] = 'Password is required!'


        return errors



class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    Email = models.CharField(max_length=255)
    Password = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()