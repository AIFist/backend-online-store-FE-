import time
from functools import wraps
from fastapi import HTTPException, Request, status
from typing import List

def rate_limited(max_calls: int, time_frame: int):
    """
    Decorator function that limits the number of calls to a function within a specified time frame.
    
    Parameters:
        max_calls (int): The maximum number of calls allowed within the time frame.
        time_frame (int): The time frame in seconds within which the maximum number of calls is enforced.
    
    Returns:
        decorator: The decorator function that wraps the original function.
    """
    def decorator(func):
        """
        Decorator function that limits the rate of calls to the wrapped function.
        
        Args:
            func: The function to be wrapped.
            request: The request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        
        Returns:
            The result of the wrapped function call.
        """
        calls = []
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            now = time.time()
            calls_in_time_frame = [call for call in calls if call > now - time_frame]
            if len(calls_in_time_frame) >= max_calls:
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
            calls.append(now)
            return await func(request, *args, **kwargs)  # Added 'await' here
        
        return wrapper
    return decorator