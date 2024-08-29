from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer, SignUpSerializer
from .throttles import FriendRequestThrottle

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    
class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'first_name', 'last_name']

    def get_queryset(self):
        search_term = self.request.query_params.get('search', '')
        if '@' in search_term:
            return User.objects.filter(email__iexact=search_term)
        return User.objects.filter(
            Q(first_name__icontains=search_term) |
            Q(last_name__icontains=search_term)
        )
    
class FriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def create(self, request, *args, **kwargs):
        # Add the authenticated user as the from_user
        request.data['from_user'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FriendRequestActionView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.to_user != request.user:
            return Response({"detail": "You can't modify this friend request."},
                            status=status.HTTP_403_FORBIDDEN)
        
        action = request.data.get('action')
        if action not in ['accept', 'reject']:
            return Response({"detail": "Invalid action."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        instance.status = 'accepted' if action == 'accept' else 'rejected'
        instance.save()
        return Response(self.get_serializer(instance).data)

class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(
            Q(sent_requests__to_user=self.request.user, sent_requests__status='accepted') |
            Q(received_requests__from_user=self.request.user, received_requests__status='accepted')
        ).distinct()
    
class PendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')