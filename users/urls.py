from django.urls import path
from .views import (
    SignUpView, CustomAuthToken, UserSearchView, FriendRequestView,
    FriendRequestActionView, FriendListView, PendingFriendRequestsView
)

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('', UserSearchView.as_view(), name='user-search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-request/<int:pk>/', FriendRequestActionView.as_view(), name='friend-request-action'),
    path('friends/', FriendListView.as_view(), name='friend-list'),
    path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-requests'),
]