from django.http import JsonResponse
from functools import wraps

def async_handler(view_func):
    @wraps(view_func)
    async def wrapper(request, *args, **kwargs):
        try:
            return await view_func(request, *args, **kwargs)
        except Exception as err:
            # Customize error handling and response here
            return JsonResponse(
                {
                    "success": False,
                    "message": str(err),
                },
                status=getattr(err, 'code', 500)  # Default to 500 if no code is provided
            )
    return wrapper
