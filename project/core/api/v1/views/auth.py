from core.api.deps import get_login_user_use_case
from core.api.v1.serializers.user import LoginRequestSerializer, LoginResponseSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login_request = serializer.to_internal_value(serializer.validated_data)

        login_user_use_case = get_login_user_use_case()
        try:
            login_response = login_user_use_case.execute(login_request)
            response_serializer = LoginResponseSerializer(instance=login_response)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
