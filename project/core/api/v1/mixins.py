from rest_framework import status
from rest_framework.response import Response


class ExecuteUseCaseOnGetMixin(object):
    use_case = None
    use_case_retrieve = None
    use_case_output = None
    use_case_output_retrieve = None
    image_fields = None
    query_serializer = None

    def get(self, request, *args, **kwargs):
        try:
            uc = self.execute_use_case_retrieve(request, *args, **kwargs)
            response = (
                uc.get_response()
                if hasattr(uc, "get_response")
                else Response(uc.data, status=status.HTTP_200_OK)
            )
            if self.image_fields:
                response = self.apply_domain_host_in_image_fields(
                    request, response, *args, **kwargs
                )
            if response.data is None:
                return Response(
                    {"detail": "object not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return response
        except self.Http400Error as e:
            print(e)
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            if hasattr(e, "code") and e.code < 500:
                return Response(
                    {"detail": e.args[0], "exception_name": e.__class__.__name__},
                    status=e.code,
                )
            raise

    def execute_use_case_retrieve(self, request, *args, **kwargs):
        use_case_class = self.get_use_case_retrieve()
        output_response = self.get_use_case_output_retrieve()
        if output_response:
            use_case_class.output_response = output_response
        uc = use_case_class(
            **self.get_use_case_kwargs_retrieve(request, *args, **kwargs)
        )
        return uc.execute()

    def get_use_case_retrieve(self):
        return self.use_case_retrieve if self.use_case_retrieve else self.use_case

    def get_use_case_kwargs_retrieve(self, request, *args, **kwargs):
        data = self.get_use_case_kwargs(request, *args, **kwargs)
        if self.query_serializer:
            serializer = self.query_serializer(data=data)
            if not serializer.is_valid():
                raise self.Http400Error(serializer.errors)
            data = {**data, **serializer.validated_data}
        return data

    def get_use_case_kwargs(self, request, *args, **kwargs):
        return {}

    def get_use_case_output_retrieve(self):
        return (
            self.use_case_output_retrieve
            if self.use_case_output_retrieve
            else self.use_case_output
        )

    def apply_domain_host_in_image_fields(self, request, response, *args, **kwargs):
        def nested_update(output_response):
            if isinstance(output_response, dict):
                for key, value in output_response.items():
                    if isinstance(value, (dict, list)):
                        nested_update(value)
                    elif key in self.image_fields:
                        output_response[key] = (
                            f"{request.scheme}://{request.get_host()}{value}"
                            if value
                            else None
                        )
            elif isinstance(output_response, list):
                for item in output_response:
                    nested_update(item)

        nested_update(response.data)
        return response

    class Http400Error(Exception):
        pass
