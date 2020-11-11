from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentication.models import UserAccount


# Register Account Serializer
class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
        }

        def create(self, validate_data):
            user = UserAccount.objects.create_user(email=validate_data['email'], password=validate_data['password'],
                                                   first_name=validate_data['first_name'],
                                                   last_name=validate_data['last_name'])
            return user


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    # password1 = serializers.CharField(write_only=True)
    # password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Password mush match.')
        return data

    def create(self, validated_data):
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password']
        return self.Meta.model.objects.create_user(**data)

    class Meta:
        model = UserAccount
        fields = '__all__'
        read_only_fields = ('id',)


class LogInSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        return token
