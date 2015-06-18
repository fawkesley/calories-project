from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    expected_daily_calories = serializers.IntegerField(
        source='user_profile.expected_daily_calories',
        required=False)

    class Meta:
        model = User
        fields = ('username', 'expected_daily_calories')

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
