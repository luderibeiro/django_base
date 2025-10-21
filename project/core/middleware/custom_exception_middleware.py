"""Handler de exceções customizado para respostas padronizadas da API.

Integra com o exception_handler do DRF e adiciona tratamento para
ValueError e IntegrityError, além de logs e traceback opcional em DEBUG.
"""

import logging
import traceback

from django.conf import settings
from django.db import IntegrityError
from django.db import utils as db_utils
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from core.domain.exceptions import EntityNotFoundException

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Formata exceções da API em respostas consistentes.

    Em caso de DEBUG, inclui traceback para facilitar diagnóstico.
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # If it is a ValidationError from DRF, it will already be handled by the default exception_handler
    # and will have a 400 status code with detailed errors.
    if response is not None and isinstance(exc, ValidationError):
        # Do nothing, default handler already formats it correctly.
        pass
    elif isinstance(exc, EntityNotFoundException):
        # Handle EntityNotFoundException as 404 Not Found
        response_data = {"detail": str(exc), "status_code": status.HTTP_404_NOT_FOUND}
        if settings.DEBUG:
            response_data["traceback"] = traceback.format_exc()
        response = Response(response_data, status=status.HTTP_404_NOT_FOUND)
    elif isinstance(exc, ValueError):
        # Handle ValueErrors from domain/use cases as 400 Bad Request
        response_data = {"detail": str(exc), "status_code": status.HTTP_400_BAD_REQUEST}
        if settings.DEBUG:
            response_data["traceback"] = traceback.format_exc()
        response = Response(response_data, status=status.HTTP_400_BAD_REQUEST)
    elif isinstance(exc, (IntegrityError, db_utils.IntegrityError)):
        response_data = {"detail": str(exc), "status_code": status.HTTP_400_BAD_REQUEST}
        if settings.DEBUG:
            response_data["traceback"] = traceback.format_exc()
        response = Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    # Now add the HTTP status code to the response if it's not already there
    if response is not None:
        if not response.data.get("status_code") and hasattr(response, "status_code"):
            response.data["status_code"] = response.status_code

        # Em modo de depuração, inclua o rastreamento completo da pilha
        if settings.DEBUG and "traceback" not in response.data:
            response.data["traceback"] = traceback.format_exc()

        # Log de exceções
        if response.status_code >= 500:
            logger.exception("Erro de servidor interno: %s", exc)
        elif response.status_code >= 400:
            logger.warning("Erro de cliente: %s", exc)

    else:
        # Captura exceções não tratadas pelo DRF ou outras exceções não processadas acima
        logger.exception("Erro inesperado: %s", exc)
        response = Response(
            {"detail": "Ocorreu um erro inesperado.", "status_code": 500},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        if settings.DEBUG:
            response.data["traceback"] = traceback.format_exc()

    return response
