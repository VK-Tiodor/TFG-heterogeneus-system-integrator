from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer

from heterogeneous_system_integrator.service.base import BaseService


class BaseViewset(ModelViewSet):
    
    SERVICE_CLASS: BaseService = None
    lookup_field = 'slug'

    def get_queryset(self):
        return self.SERVICE_CLASS.create_query()
    
    def get_object(self):
        return self.SERVICE_CLASS.get(filters={self.lookup_field: self.kwargs[self.lookup_field]})
    
    def perform_create(self, serializer: ModelSerializer):
        return self.SERVICE_CLASS.insert(properties=serializer.data)
    
    def perform_update(self, serializer: ModelSerializer):
        return self.SERVICE_CLASS.update(filters={self.lookup_field: serializer.data[self.lookup_field]}, new_values=serializer.data)
    
    def perform_destroy(self, instance):
        return self.SERVICE_CLASS.delete(model=instance)