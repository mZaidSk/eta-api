from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from .models import Account
from .serializers import AccountSerializer
from eta_api.utils.responses import success_response, error_response


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # GET /accounts/
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)

    # GET /accounts/{id}/
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return success_response(serializer.data)

    # POST /accounts/
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return success_response(
                serializer.data,
                message="Account created successfully",
                status=status.HTTP_201_CREATED,
            )
        return error_response(serializer.errors, message="Validation failed")

    # PUT /accounts/{id}/
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                serializer.data, message="Account updated successfully"
            )
        return error_response(serializer.errors, message="Validation failed")

    # PATCH /accounts/{id}/
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(
                serializer.data, message="Account partially updated successfully"
            )
        return error_response(serializer.errors, message="Validation failed")

    # DELETE /accounts/{id}/
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response(message="Account deleted successfully", data=None)
