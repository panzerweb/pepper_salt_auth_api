from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, LoginSerializer
from .services import register_user, login_user

# Create your views here.
class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        register_user(**serializer.validated_data)

        return Response({
            "message": "Registered successfully",
            "status": status.HTTP_201_CREATED
        }, status=status.HTTP_201_CREATED)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = login_user(**serializer.validated_data)

        if not user:
            return Response({"error": "Invalid credentials", "status":status.HTTP_401_UNAUTHORIZED}, status=401)

        return Response({
            "message": "Login successful",
            "email": user.email,
            "status": status.HTTP_200_OK
        }, status=status.HTTP_200_OK)