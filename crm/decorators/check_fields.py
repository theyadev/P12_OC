from rest_framework.response import Response

def check_fields(required_fields):
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            missing_fields = []

            for field in required_fields:
                if not field in request.data:
                    missing_fields.append(field)

            if missing_fields:
                return Response(status=400, data={'error': f'Missing required fields in body. ({", ".join(missing_fields)})'})

            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator
