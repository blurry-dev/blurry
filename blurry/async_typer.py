import asyncio
from functools import wraps

from typer import Typer


class AsyncTyper(Typer):
    def async_command(self, *args, **kwargs):
        def decorator(async_func):
            # Convert async function to synchronous
            @wraps(async_func)
            def sync_func(*_args, **_kwargs):
                return asyncio.run(async_func(*_args, **_kwargs))

            # Register synchronous function
            self.command(*args, **kwargs)(sync_func)

            return async_func

        return decorator
