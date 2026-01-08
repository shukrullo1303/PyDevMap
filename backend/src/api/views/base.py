from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser,  AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas

from django.contrib.auth.models import AnonymousUser

from src.core.models import *
from src.api.serializers import *
from src.api.views.utils import can_user_open_lesson
from src.shared.pagination import *
from src.api.permission import IsAdminOnly


class BaseViewSet(ModelViewSet):
    """
    A base view set that provides default `list()`, `create()`, `retrieve()`,
    `update()`, and `destroy()` actions.
    """
