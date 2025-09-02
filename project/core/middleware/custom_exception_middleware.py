import logging
import traceback

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        # Adicione o código de status HTTP à resposta se não estiver presente
        if not response.data.get("status_code"):
            response.data["status_code"] = response.status_code

        # Personalize a mensagem de erro para exceções específicas
        if isinstance(exc, ValueError):
            response.data["detail"] = str(exc)
            response.status_code = status.HTTP_400_BAD_REQUEST

        # Em modo de depuração, inclua o rastreamento completo da pilha
        if settings.DEBUG:
            response.data["traceback"] = traceback.format_exc()

        # Log de exceções
        if response.status_code >= 500:
            logger.exception("Erro de servidor interno: %s", exc)
        elif response.status_code >= 400:
            logger.warning("Erro de cliente: %s", exc)

    else:
        # Captura exceções não tratadas pelo DRF
        logger.exception("Erro inesperado: %s", exc)
        response = Response(
            {"detail": "Ocorreu um erro inesperado.", "status_code": 500},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        if settings.DEBUG:
            response.data["traceback"] = traceback.format_exc()

    return response
