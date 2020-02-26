from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.validators import UniqueValidator

from user.models import EmailUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    error_messages = {
        'password_mismatch': _('The two password fields did NOT match.'),
    }
    password1 = serializers.CharField(
        label=_("Password"),
        trim_whitespace=False,
        required=False,
        write_only=True,
        min_length=5,
        help_text=_("Enter the password for your account."),
    )
    password2 = serializers.CharField(
        label=_("Password confirmation"),
        trim_whitespace=False,
        required=False,
        write_only=True,
        min_length=5,
        help_text=_("Enter the same password again, for verification."),
    )
    email = serializers.EmailField(label='Email', max_length=254,
                                   validators=[UniqueValidator(queryset=EmailUser.objects.all(),
                                                               message='Unable to sign in with provided credentials.')])

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}, }

    def validate(self, attrs):
        password1 = attrs.get("password1", None)
        password2 = attrs.get("password2", None)
        if password1 and password2 and password1 != password2:
            raise serializers.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return attrs

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        validated_data.pop('password1', None)
        password = validated_data.pop('password2', None)
        return get_user_model().objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        validated_data.pop('password1', None)
        password = validated_data.pop('password2', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class EmailAuthTokenSerializer(AuthTokenSerializer):
    username = None
    email = serializers.EmailField(label=_("Email"), min_length=5, )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
