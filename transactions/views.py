from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.db.models import Sum
from decimal import Decimal
from .models import Transaction
from .serializers import RegisterSerializer, TransactionSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response({'message': 'User registered successfully','user': serializer.data},status=status.HTTP_201_CREATED )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        return Response(
            {'message': 'Login successful'},
            status=status.HTTP_200_OK
        )

    return Response({'error': 'Invalid username or password'},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    request.auth.delete()

    return Response(
        {'message': 'Logout successful'},
        status=status.HTTP_200_OK
    )


@api_view(['GET', 'POST'])
def transactions(request):
    if request.method == 'GET':

        transaction_type = request.query_params.get('type')

        data = Transaction.objects.filter(user=request.user)

        if transaction_type:

            if transaction_type not in ['income', 'expense']:
                return Response(
                    {'error': 'Type must be income or expense'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            data = data.filter(type=transaction_type)

        serializer = TransactionSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':

        serializer = TransactionSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(user=request.user)

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



@api_view(['GET', 'PUT', 'DELETE'])
def transaction_detail(request, pk):
    transaction = Transaction.objects.filter(
        pk=pk,
        user=request.user
    ).first()

    if transaction is None:
        return Response(
            {'error': 'Transaction not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':

        serializer = TransactionSerializer(transaction)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':

        serializer = TransactionSerializer(
            transaction,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':

        transaction.delete()

        return Response(
            {'message': 'Transaction deleted successfully'},
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
def summary(request):
    income = Transaction.objects.filter(
        user=request.user,
        type='income'
    ).aggregate(total=Sum('amount'))['total']

    expense = Transaction.objects.filter(
        user=request.user,
        type='expense'
    ).aggregate(total=Sum('amount'))['total']

    if income is None:
        income = Decimal('0.00')

    if expense is None:
        expense = Decimal('0.00')

    balance = income - expense

    return Response(
        {
            'total_income': income,
            'total_expense': expense,
            'balance': balance
        },
        status=status.HTTP_200_OK
    )
