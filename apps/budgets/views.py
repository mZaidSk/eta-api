from rest_framework import viewsets, permissions, status
from .models import Budget
from .serializers import BudgetSerializer
from eta_api.utils.responses import success_response, error_response


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only budgets for logged-in user
        return Budget.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        # Attach logged-in user automatically
        serializer.save(user=self.request.user)

    # 👇 Override CRUD methods with custom responses
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
                message="Budget created successfully",
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
                serializer.data, message="Budget updated successfully"
            )
        return error_response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            message="Validation failed",
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(None, message="Budget deleted successfully")
