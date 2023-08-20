from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    surname = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('surname', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # If surname is not provided, generate it
        if 'surname' not in validated_data:
            base_surname = f"{validated_data['first_name']}_{validated_data['last_name']}".strip()
            suffix = 1
            generated_surname = base_surname

            while User.objects.filter(surname=generated_surname).exists():
                generated_surname = f"{base_surname}_{suffix}"
                suffix += 1

            validated_data['surname'] = generated_surname

        user = User.objects.create(
            surname=validated_data['surname'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'date_joined', 'first_name',
                  'last_name', 'email', 'password', 'surname']


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'surname']

