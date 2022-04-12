from django.urls import path
from rest_framework.routers import DefaultRouter

from network_app.views import SignUp, PostViewSet, AnaliticsView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')


urlpatterns = [
    path('sign_up/', SignUp.as_view(), name='sign-up'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('analitics/', AnaliticsView.as_view(), name='analitics'),
]

urlpatterns += router.urls



