from rest_framework import serializers
from .models import User, FriendRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']

    def validate(self, data):
        # Ensure users can't send friend requests to themselves
        if data['to_user'] == self.context['request'].user:
            raise serializers.ValidationError("You can't send a friend request to yourself.")
        
        # Check if a friend request already exists
        if FriendRequest.objects.filter(from_user=self.context['request'].user, to_user=data['to_user']).exists():
            raise serializers.ValidationError("A friend request to this user already exists.")

        return data
class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user