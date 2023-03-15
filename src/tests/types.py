from typing import Callable

from django.http import HttpResponse

CT = Callable[..., HttpResponse]
