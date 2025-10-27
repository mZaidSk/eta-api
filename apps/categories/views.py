from rest_framework import viewsets, permissions, status
from .models import Category
from .serializers import CategorySerializer
from eta_api.utils.responses import (
    success_response,
    error_response,
)  # 👈 import helpers


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return categories belonging to the logged-in user
        return Category.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        # Attach the logged-in user automatically
        serializer.save(user=self.request.user)

    # 👇 Override list, retrieve, create, update, destroy to use your helper
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return success_response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                message="Category created successfully",
            )
        return error_response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            message="Validation failed",
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return success_response(
                serializer.data, message="Category updated successfully"
            )
        return error_response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            message="Validation failed",
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(None, message="Category deleted successfully")
