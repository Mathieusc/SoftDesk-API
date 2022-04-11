from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email"]


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Register new user
    attributes : email is required and should be unique amongst all user
                 password is write only, required and should be valid
                 password_confirm is write only and required
    """

    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "password_confirm",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        """
        Verifiy that password fields are the same.
        """
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "Votre mot de passe ne correspond pas."}
            )
        return attrs

    def create(self, validated_data):
        """
        When send POST request to register endpoint,
        it calls RegisterUserSerializer's create method which saves user object.
        """
        user = User(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user
