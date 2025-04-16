# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'sales_person', 'password'
        ]

    # this create method overload hashes the password
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # pops the password out of the request body
        password = validated_data.pop('password', None)

        # Update all the other fields normally
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # If password was provided, hash it
        if password:
            instance.set_password(password)

        instance.save()
        return instance