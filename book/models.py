from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

phone_regex = RegexValidator(regex=r'^[\d\(\)\- ]{7,15}$',
                             message=_("Номер должен быть следующего формата: '+99999999'. Не больше 15 цифр"))


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    name = models.CharField(_('Имя'), max_length=64, blank=False)
    surname = models.CharField(_('Фамилия'), max_length=64, blank=False)
    patronymic = models.CharField(_('Отчество'), max_length=64, blank=False)
    address = models.TextField(_('Адрес'), blank=False)
    phone_number = models.CharField(_('Телефон'), max_length=64, validators=[], blank=True)
    email = models.EmailField(_('Электронная почта'), blank=True)
    comment = models.TextField(_('Комментарий'), blank=True)





