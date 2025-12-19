from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'role',
            'role_name',
            'first_name',
            'last_name',
        ]

    def get_role_name(self, obj):
        # SAFE: works even if role is None
        if obj.role is None:
            return None
        return obj.get_role_display()
