from django.contrib.auth.models import User
from rest_framework import generics, permissions

from apps.meals.serializers import UserSerializer


class UserList(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)  # Bearing in mind it's create-only

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return User.objects.all()

        return User.objects.filter(pk=user.pk)
