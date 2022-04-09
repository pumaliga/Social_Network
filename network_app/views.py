from rest_framework import permissions, status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from network_app.models import CustomUser, Post
from network_app.serializer import SignUpSerializer, PostSerializer, FanSerializer
from network_app.tools import add_like, remove_like, get_fans, clear_data


class LikedMixin:
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
        creates a like for a post from a user
        """
        obj = self.get_object()
        add_like(obj, request.user)

        return Response({'post_id': obj.id, 'action': 'like'},
                        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        """
        delete a like for a post from a user
        """
        obj = self.get_object()
        remove_like(obj, request.user)

        return Response({'post_id': obj.id, 'action': 'unlike'},
                        status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['get'])
    def get_fans(self, request, pk=None):
        """
        get all users who liked this post
        """
        obj = self.get_object()
        fans = get_fans(obj)
        print(obj, 'obj')
        print(fans, 'fans')
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data)


class SignUp(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        lookup = clear_data(response.data["email"])
        print(lookup)
        return Response({'message': 'Sign up access',
                         'username': response.data.get('username'),
                         'email': response.data.get('email')},
                         status=status.HTTP_201_CREATED)


class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]

    def destroy(self, request, *args, **kwargs):
        """
        only the author of the post or the admin can delete a post
        """
        serializer = self.get_serializer(self.get_object())
        author_id = serializer.data.get('author').get('id')
        user = self.request.user
        if user.id == author_id or user.is_superuser:
            super().destroy(request, *args, **kwargs)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        raise serializers.ValidationError(
            {"detail": "You do not have permission to perform this action or you did not create this post"})

    def update(self, request, *args, **kwargs):
        """
        only the author of the post can update a post
        """
        serializer = self.get_serializer(self.get_object())
        author_id = serializer.data.get('author').get('id')
        user = self.request.user
        if user.id == author_id:
            super().update(request, *args, **kwargs)
            return Response(serializer.data, status=status.HTTP_200_OK)

        raise serializers.ValidationError(
            {"detail": "you did not create this post"})

    def partial_update(self, request, *args, **kwargs):
        """
        only the author of the post can partial update a post
        """
        serializer = self.get_serializer(self.get_object())
        author_id = serializer.data.get('author').get('id')
        user = self.request.user
        if user.id == author_id:
            super().partial_update(request, *args, **kwargs)
            return Response(serializer.data, status=status.HTTP_200_OK)

        raise serializers.ValidationError(
            {"detail": "you did not create this post"})


