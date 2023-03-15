from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from account.models import Profile, User
from utils.base.general import get_tokens_for_user

from . import serializers
from .permissions import PermA, PermB
from .tokens import account_confirm_token


class TokenVerifyAPIView(APIView):
    """
    An authentication plugin that checks if a jwt
    access token is still valid and returns the user info.
    """

    permission_classes = (PermA,)

    @swagger_auto_schema(
        request_body=serializers.JWTTokenValidateSerializer,
        responses={200: serializers.UserSerializer}
    )
    def post(self, request, format=None):
        jwt_auth = JWTAuthentication()

        raw_token = request.data.get('token')

        validated_token = jwt_auth.get_validated_token(raw_token)

        user = jwt_auth.get_user(validated_token)

        serialized_user = serializers.UserSerializer(user)
        user_details = serialized_user.data

        return Response(data=user_details)


class TokenRefreshAPIView(APIView):
    permission_classes = (PermA,)
    serializer_class = TokenRefreshSerializer

    @swagger_auto_schema(
        request_body=TokenRefreshSerializer,
        responses={200: TokenRefreshSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = (PermA,)
    serializer_class = serializers.LoginSerializer

    @swagger_auto_schema(
        request_body=serializers.LoginSerializer,
        responses={
            200: serializers.LoginResponseSerializer200,
            431: serializers.LoginResponseSerializer431
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')

            user = User.objects.get(email=email)

            if user.is_active:
                if user.verified_email:
                    # Get the user details with the user serializer
                    s2 = serializers.UserSerializer(user)

                    user_details = s2.data
                    response_data = {
                        'tokens': get_tokens_for_user(user),
                        'user': user_details
                    }
                    # return Response(data=response_data)
                    return Response(data=response_data)
                else:
                    # Get email tokens for user
                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    # Generate token for this user
                    token = account_confirm_token.make_token(user)
                    tokens = {
                        'uidb64': uidb64,
                        'token': token,
                    }

                    # full Response
                    response_data = {
                        'tokens': tokens,
                        'fullname': user.profile.get_fullname,
                        'email': user.email,
                    }

                    return Response(data=response_data, status='431')
            else:
                return Response(status='432')
        else:
            return Response(data=serializer.errors, status='400')


class ForgetPasswordView(APIView):
    permission_classes = (PermA,)

    @swagger_auto_schema(
        responses={
            200: serializers.LoginResponseSerializer431
        }
    )
    def post(self, request, *args, **kwargs):
        email = kwargs.get('email')

        try:
            user = User.objects.get(email=email)

            # Get email tokens for user
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # Generate token for this user
            token = account_confirm_token.make_token(user)
            tokens = {
                'uidb64': uidb64,
                'token': token,
            }

            # full Response
            response_data = {
                'tokens': tokens,
                'fullname': user.profile.get_fullname,
                'email': user.email,
            }

            return Response(data=response_data, status='200')

        except User.DoesNotExist:
            # User email does not exist
            pass

        return Response(status='424')


class RegisterAPIView(APIView):
    permission_classes = (PermA,)
    serializer_class = serializers.RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Get the user details with the user serializer
            user_serializer = serializers.UserSerializer(user)

            # Get email tokens for user
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            # Generate token for this user
            token = account_confirm_token.make_token(user)
            tokens = {
                'uidb64': uidb64,
                'token': token
            }
            user_details = user_serializer.data

            response_data = {
                'tokens': tokens,
                'user': user_details
            }

            return Response(data=response_data, status='201')

        return Response(data=serializer.errors, status='400')

    @swagger_auto_schema(
        request_body=serializers.RegisterSerializer,
        responses={201: serializers.RegisterResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    permission_classes = (PermB,)
    serializer_class = serializers.ProfileSerializer
    http_method_names = ['get', 'patch']

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user.id)

    def get_queryset(self):
        return Profile.objects.all()


class ForgetChangePasswordView(generics.UpdateAPIView):
    permission_classes = (PermA,)
    serializer_class = serializers.ForgetChangePasswordSerializer

    http_method_names = ['patch']

    def get_object(self):
        return self.object

    @swagger_auto_schema(
        request_body=serializers.ForgetChangePasswordSerializerSwagger,
    )
    def patch(self, request, *args, **kwargs):
        # Get the uid and token from the data passed
        uidb64 = request.data.get('uidb64', '')
        token = request.data.get('token', '')

        try:
            uidb64 = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uidb64)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            error = Response(status='427')
            return error

        # Validate the token
        if user is not None:
            if account_confirm_token.check_token(user, token):
                self.object = user
                return super().patch(request, *args, **kwargs)

        error = Response(status='425')
        return error

    def get_queryset(self):
        return User.objects.filter(active=True)


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (PermB,)
    serializer_class = serializers.ChangePasswordSerializer
    http_method_names = ['patch']

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return User.objects.filter(active=True)


class UserListView(generics.ListAPIView):
    permission_classes = (PermB,)
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return User.objects.all().order_by('email')


class UserAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (PermB,)
    serializer_class = serializers.UserSerializer
    http_method_names = ['get', 'patch']

    def get_queryset(self):
        return User.objects.all()

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        # Get the user data
        response_data = self.get_serializer_class()(request.user).data
        return Response(data=response_data)
