from django.db.models import Q
from rest_framework.serializers import ModelSerializer, \
                                       ValidationError, \
                                       EmailField

from rest_framework.status import HTTP_200_OK, \
                                  HTTP_400_BAD_REQUEST, \
                                  HTTP_401_UNAUTHORIZED

from base.models import *

class CleanerCreateSerializer(ModelSerializer):
    class Meta:
        model = Cleaner
        fields = ('first_name', 'last_name', 'city')       