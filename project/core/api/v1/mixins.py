from rest_framework import status
from rest_framework.response import Response


class ExecuteUseCaseOnGetMixin:
    """
    Mixin para executar casos de uso ao lidar com solicitações GET.
    """

    def get(self, request, *args, **kwargs):
        """
        Manipula solicitações GET.

        Args:
        ----
            request: Objeto de solicitação HTTP.
            *args: Argumentos posicionais adicionais.
            **kwargs: Argumentos de palavra-chave adicionais.

        Returns:
        -------
            Resposta HTTP.
        """
        try:
            uc = self.execute_use_case_retrieve(request, *args, **kwargs)
            response = getattr(uc, "get_response", lambda: Response(uc.data))()
            if self.image_fields:
                response = self.apply_domain_host_in_image_fields(request, response, *args, **kwargs)
            if not response.data:
                return Response(
                    {"detail": "object not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return response
        except self.Http400Error as e:
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            if getattr(e, "code", None) and e.code < 500:
                return Response(
                    {"detail": e.args[0], "exception_name": e.__class__.__name__},
                    status=e.code,
                )
            raise

    def execute_use_case_retrieve(self, request, *args, **kwargs):
        """
        Executa o caso de uso do método retrieve.

        Args:
        ----
            request: Objeto de solicitação HTTP.
            *args: Argumentos posicionais adicionais.
            **kwargs: Argumentos de palavra-chave adicionais.

        Returns:
        -------
            Instância do caso de uso.
        """
        use_case_class = self.get_use_case_retrieve()
        output_response = self.get_use_case_output_retrieve()
        if output_response:
            use_case_class.output_response = output_response
        uc = use_case_class(**self.get_use_case_kwargs_retrieve(request, *args, **kwargs))
        return uc.execute()

    def get_use_case_retrieve(self):
        """
        Obtém a classe de caso de uso do método retrieve.

        Returns:
        -------
            Classe de caso de uso.
        """
        return getattr(self, "use_case_retrieve", self.use_case)

    def get_use_case_kwargs_retrieve(self, request, *args, **kwargs):
        """
        Obtém os argumentos do caso de uso do método retrieve.

        Args:
        ----
            request: Objeto de solicitação HTTP.
            *args: Argumentos posicionais adicionais.
            **kwargs: Argumentos de palavra-chave adicionais.

        Returns:
        -------
            Argumentos do caso de uso.
        """
        data = self.get_use_case_kwargs(request, *args, **kwargs)
        if self.query_serializer:
            serializer = self.query_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            data.update(serializer.validated_data)
        return data

    def get_use_case_kwargs(self, request, *args, **kwargs):
        """
        Obtém os argumentos do caso de uso.

        Args:
        ----
            request: Objeto de solicitação HTTP.
            *args: Argumentos posicionais adicionais.
            **kwargs: Argumentos de palavra-chave adicionais.

        Returns:
        -------
            Argumentos do caso de uso.
        """
        return {}

    def get_use_case_output_retrieve(self):
        """
        Obtém a saída do caso de uso do método retrieve.

        Returns:
        -------
            Saída do caso de uso.
        """
        return getattr(self, "use_case_output_retrieve", self.use_case_output)

    def apply_domain_host_in_image_fields(self, request, response, *args, **kwargs):
        """
        Aplica o domínio e o host nos campos de imagem na resposta.

        Args:
        ----
            request: Objeto de solicitação HTTP.
            response: Resposta HTTP.
            *args: Argumentos posicionais adicionais.
            **kwargs: Argumentos de palavra-chave adicionais.

        Returns:
        -------
            Resposta HTTP com domínio e host aplicados nos campos de imagem.
        """

        def nested_update(output_response):
            if isinstance(output_response, dict):
                for key, value in output_response.items():
                    if isinstance(value, dict | list):
                        nested_update(value)
                    elif key in self.image_fields:
                        output_response[key] = (
                            f"{request.scheme}://{request.get_host()}{value}" if value else None
                        )
            elif isinstance(output_response, list):
                for item in output_response:
                    nested_update(item)

        nested_update(response.data)
        return response

    class Http400Error(Exception):
        """
        Exceção para erros de solicitação HTTP 400.
        """

        def __init__(self, message):
            super().__init__(message)
            self.message = message
