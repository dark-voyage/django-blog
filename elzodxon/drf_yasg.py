from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Elzodxon's blog API",
      default_version='v1',
      description="This is Elzodxon's blog API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="itstoolongname@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
