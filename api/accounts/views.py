from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterSerializer, LoginSerializer
from .services import register_user, login_user

# View for handling user registration
class RegisterView(GenericAPIView):
    # Assign serializer used for validating incoming data
    serializer_class = RegisterSerializer

    def post(self, request):
        # Initialize serializer with request data
        serializer = self.get_serializer(data=request.data)

        # Validate data (raises error automatically if invalid)
        serializer.is_valid(raise_exception=True)

        # Call service layer to create user (handles hashing, salt, pepper)
        register_user(**serializer.validated_data)

        # Return success response
        return Response(
            {"message": "Registered successfully", "status": status.HTTP_201_CREATED},
            status=status.HTTP_201_CREATED,
        )


# View for handling user login
class LoginView(GenericAPIView):
    # Assign serializer for login input validation
    serializer_class = LoginSerializer

    def post(self, request):
        # Initialize serializer with request data
        serializer = self.get_serializer(data=request.data)

        # Validate input credentials format
        serializer.is_valid(raise_exception=True)

        # Call service layer to authenticate user
        user = login_user(**serializer.validated_data)

        # If authentication fails, return error response
        if not user:
            return Response(
                {
                    "error": "Invalid credentials",
                    "status": status.HTTP_401_UNAUTHORIZED,
                },
                status=401,
            )

        # If successful, return user info (basic response)
        return Response(
            {
                "message": "Login successful",
                "username": user.username,
                "status": status.HTTP_200_OK,
            },
            status=status.HTTP_200_OK,
        )