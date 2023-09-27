from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
#from rest_framework.pagination import LimitOffsetPagination

from djoser.views import UserViewSet

from users.models import Subscription
from users.serializers import CustomUserSerializer, SubscriptionSerializer


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # def get_serializer_class(self):
    #     if self.action == "subscriptions":
    #         return self.serializer_class
    #     elif self.action == "subscribe_unsubscribe":
    #         return SubscriptionSerializer
    #     else:
    #         return self.serializer_class


    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    @action(detail=False,
            permission_classes=(permissions.IsAuthenticated, ),
            )
    def subscriptions(self, request):
        favourive_authors = request.user.fav_authors.all()
        serializer = CustomUserSerializer(
            favourive_authors,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(permissions.IsAuthenticated, ),
            url_path=r'subscribe',
            )
    def subscribe_unsubscribe(self, request, id):
        author = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            sub_serializer = SubscriptionSerializer(
                data={'author': author},
                context={'request': request}
            )
            sub_serializer.is_valid(raise_exception=True)
            sub_serializer.save(user=self.request.user)
            return Response(sub_serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        # if request.method == 'DELETE':
        #     subscription = get_object_or_404(Subscription, user=current_user, author=author)
        #     subscription.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)


# class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = CustomUserSerializer

#     def get_queryset(self):
#         return self.request.user.fav_authors.all()


