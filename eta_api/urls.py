from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


# --- Custom error handlers ---
def custom_404(request, exception=None):
    return JsonResponse({"error": "Not Found", "status_code": 404}, status=404)


def custom_500(request):
    return JsonResponse(
        {"error": "Internal Server Error", "status_code": 500}, status=500
    )


# Tell Django to use these handlers
handler404 = "eta_api.urls.custom_404"
handler500 = "eta_api.urls.custom_500"


# --- Routes ---
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]
