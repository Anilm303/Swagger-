from django.contrib.auth import authenticate
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from drf_spectacular.utils import extend_schema

from .authentication import generate_token
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    TokenResponseSerializer,
    MessageSerializer,
)

# ─────────────────────────────────────────────
# Register
# ─────────────────────────────────────────────
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Register a new user",
        description="Create a new user account and return JWT token",
        request=RegisterSerializer,
        responses={201: TokenResponseSerializer},
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_token(user)

            return Response({
                "token": token,
                "token_type": "Bearer",
                "expires_in": settings.JWT_EXPIRY_HOURS * 3600,
                "user": UserProfileSerializer(user).data,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────────
# Login
# ─────────────────────────────────────────────
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Login user",
        request=LoginSerializer,
        responses={200: TokenResponseSerializer},
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )

            if user:
                token = generate_token(user)

                return Response({
                    "token": token,
                    "token_type": "Bearer",
                    "expires_in": settings.JWT_EXPIRY_HOURS * 3600,
                    "user": UserProfileSerializer(user).data,
                })

            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────────
# Logout
# ─────────────────────────────────────────────
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Logout user",
        request=None,
        responses={200: MessageSerializer},
        tags=["User"],
    )
    def post(self, request):
        return Response({
            "message": "Logged out successfully"
        })


# ─────────────────────────────────────────────
# Profile
# ─────────────────────────────────────────────
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Get user profile",
        responses={200: UserProfileSerializer},
        tags=["User"],
    )
    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)

    @extend_schema(
        summary="Update user profile",
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer},
        tags=["User"],
    )
    def patch(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────────
# Change Password
# ─────────────────────────────────────────────
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Change password",
        request=ChangePasswordSerializer,
        responses={200: TokenResponseSerializer},
        tags=["User"],
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not request.user.check_password(serializer.validated_data["old_password"]):
                return Response(
                    {"error": "Old password is incorrect"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            request.user.set_password(serializer.validated_data["new_password"])
            request.user.save()

            token = generate_token(request.user)

            return Response({
                "token": token,
                "token_type": "Bearer",
                "expires_in": settings.JWT_EXPIRY_HOURS * 3600,
                "user": UserProfileSerializer(request.user).data,
                "message": "Password changed successfully"
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ─────────────────────────────────────────────
# Verify Token
# ─────────────────────────────────────────────
class VerifyTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="Verify token",
        responses={200: MessageSerializer},
        tags=["Authentication"],
    )
    def get(self, request):
        return Response({
            "valid": True,
            "user": UserProfileSerializer(request.user).data
        })