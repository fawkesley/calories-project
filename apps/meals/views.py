from django.contrib.auth.models import User
from rest_framework import generics, permissions, exceptions

from apps.meals.serializers import MealSerializer, UserSerializer
from apps.meals.models import Meal


class MealGetQuerySetMixin(object):
    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        query_username = self.kwargs['username']
        requesting_user = self.request.user

        if requesting_user.username != query_username:
            if not requesting_user.is_superuser:
                raise exceptions.PermissionDenied

        return Meal.objects.filter(owner__username=query_username)


class MealList(MealGetQuerySetMixin, generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    serializer_class = MealSerializer

    def perform_create(self, serializer):
        """
        See http://www.django-rest-framework.org/api-guide/generic-views/
        under "Save and deletion hooks"

        Attach the current user to the serializer before saving.
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super(MealList, self).get_queryset()

        from_date = self.request.query_params.get('from_date', None)
        to_date = self.request.query_params.get('to_date', None)
        from_time = self.request.query_params.get('from_time', None)
        to_time = self.request.query_params.get('to_time', None)

        if from_date is not None:
            queryset = queryset.filter(date__gte=from_date)

        if to_date is not None:
            queryset = queryset.filter(date__lte=to_date)

        if from_time is not None:
            queryset = queryset.filter(time__gte=from_time)

        if to_time is not None:
            queryset = queryset.filter(time__lte=to_time)

        return queryset



class UserList(generics.CreateAPIView):
    # Bearing in mind it's create-only
    permission_classes = (permissions.AllowAny,)

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
