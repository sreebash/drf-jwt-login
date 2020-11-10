from rest_framework import serializers

from authentication.models import UserAccount


# Register Account Serializer
class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'
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
    class Meta:
        model = UserAccount
        fields = '__all__'
