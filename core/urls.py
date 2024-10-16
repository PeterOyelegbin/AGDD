"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from accounts.views import *
from directdebit.views import *
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Alert Group Direct Debit API",
      default_version='v1',
      description="This is a backend system for Alert Group Direct Debit application where staff can sign up, log in, create mandate, and track mandate with JWT authentication feature.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="peteroyelegbin@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("admin", admin.site.urls),

    # User authentication routes (API)
    path('api/v1/auth/login', LoginView.as_view(), name='user_login'),
    path('api/v1/auth/logout', LogoutView.as_view(), name='user_logout'),
    path('api/v1/auth/password/reset', PasswordResetView.as_view(), name='password_reset'),
    path('api/v1/auth/password/confirm', PasswordConfirmView.as_view(), name='password_confirm'),
    
    # User profile routes (API)
    path('api/v1/account/users', UserListCreateView.as_view(), name='users'),
    path('api/v1/account/users/<pk>', UserRetrUpdtDelView.as_view(), name='manage_users'),

    # Mandate routes (API)
    path('api/v1/mandates/create', CreateMandateView.as_view(), name='create_mandate'),
    path('api/v1/mandates/balance', BalanceEnquiryView.as_view(), name='mandate_balance'),
    path('api/v1/mandates/e-mandate', CreateEMandateView.as_view(), name='create_e_mandate'),
    path('api/v1/mandates/fetch/<str:page>/<str:pageSize>', FetchMandateView.as_view(), name='fetch_mandates'),
    path('api/v1/mandates/status', MandateStatusView.as_view(), name='mandate_status'),
    path('api/v1/mandates/update', UpdateMandateStatusView.as_view(), name='update_mandate_status'),
    
    # Biller routes (API)
    path('api/v1/biller/product/<int:id>', GetProductView.as_view(), name='get_product'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
