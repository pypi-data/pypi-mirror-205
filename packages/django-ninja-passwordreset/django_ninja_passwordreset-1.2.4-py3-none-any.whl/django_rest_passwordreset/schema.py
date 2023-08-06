from datetime import timedelta

from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from ninja import Schema
from pydantic import EmailStr, root_validator

from . import models

__all__ = [
    "EmailSerializer",
    "PasswordTokenSerializer",
    "ResetTokenSerializer",
]


class EmailSerializer(Schema):
    email: EmailStr


class PasswordValidateMixin(Schema):
    @root_validator
    def password_validate(cls, values):
        token = values.get("token")

        # get token validation time
        password_reset_token_validation_time = (
            models.get_password_reset_token_expiry_time()
        )

        # find token
        try:
            reset_password_token = _get_object_or_404(
                models.ResetPasswordToken, key=token
            )
        except (
            TypeError,
            ValueError,
            ValidationError,
            Http404,
            models.ResetPasswordToken.DoesNotExist,
        ):
            raise Http404(
                _("The OTP password entered is not valid. Please check and try again.")
            )

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(
            hours=password_reset_token_validation_time
        )

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            raise Http404(_("The token has expired"))
        return values


class PasswordTokenSerializer(PasswordValidateMixin):
    password: str
    token: str


class ResetTokenSerializer(PasswordValidateMixin):
    token: str
