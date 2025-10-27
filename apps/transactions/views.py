from rest_framework import viewsets, permissions, status
from .models import Transaction, RecurringTransaction
from .serializers import TransactionSerializer, RecurringTransactionSerializer
from eta_api.utils.responses import success_response, error_response


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # 👇 Override CRUD methods with custom responses
    def list(self, request, *args, **kwargs):
        print("TransactionViewSet initialized")

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
                message="Transaction created successfully",
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
                serializer.data, message="Transaction updated successfully"
            )
        return error_response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            message="Validation failed",
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(None, message="Transaction deleted successfully")


class RecurringTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = RecurringTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    # print("RecurringTransactionViewSet initialized")

    def get_queryset(self):
        return RecurringTransaction.objects.filter(user=self.request.user).order_by(
            "-start_date"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # 👇 Override CRUD methods with custom responses
    def list(self, request, *args, **kwargs):
        print("RecurringTransactionViewSet initialized")

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
                message="Recurring transaction created successfully",
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
                serializer.data, message="Recurring transaction updated successfully"
            )
        return error_response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
            message="Validation failed",
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return success_response(
            None, message="Recurring transaction deleted successfully"
        )
