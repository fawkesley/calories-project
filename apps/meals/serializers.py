from django.contrib.auth.models import User

from rest_framework import serializers
from apps.meals.models import Meal


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id', 'date', 'time', 'description', 'calories')


class UserSerializer(serializers.ModelSerializer):
    expected_daily_calories = serializers.IntegerField(
        source='user_profile.expected_daily_calories',
        required=False)

    class Meta:
        model = User
        fields = ('username', 'expected_daily_calories', 'password')
        extra_kwargs = {'password': {'required': False, 'write_only': True}}

    def create(self, validated_data):
        # The `create_user` helper handles hashing passwords.
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        By default, Django rest framework tries to replace the `user_profile`
        rather than simply updating the `expected_daily_calories` field on it.
        """
        try:
            user_profile = validated_data.pop('user_profile')
        except KeyError:
            pass
        else:
            instance.user_profile.expected_daily_calories = user_profile[
                'expected_daily_calories']
            instance.user_profile.save()

        return super(UserSerializer, self).update(instance, validated_data)
