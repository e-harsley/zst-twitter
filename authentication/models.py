from django.contrib.auth import get_user_model
from django.db import models
from helpers.models import TrackingModel
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from authentication.manager import UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

class User(AbstractBaseUser, PermissionsMixin, TrackingModel):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=False,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        }
    )
    email = models.EmailField(_('email address'),  blank=False, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    email_verified = models.BooleanField(
        _('email_verified'),
        default=False,
        help_text=_(
            'Designates whether this users email is verified. '

        ),
    )
    phone_number = models.CharField(_('phone number'),
                                    max_length=150,
                                    unique=True,
                                    blank=False,
                                    error_messages={
                                        'unique': _("A user with that phone number already exists."),
                                    }
                                    )
    first_name = models.CharField(_('first name'), blank=False,max_length=150)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    # REQUIRED_FIELDS = ['username']

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Contact(models.Model):
    user_from = models.ForeignKey(User,
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey(User,
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)


    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'

# user_model = get_user_model()

User.add_to_class('following',
                            models.ManyToManyField('self',
                                                   through=Contact,
                                                   related_name='followers',
                                                   symmetrical=False))