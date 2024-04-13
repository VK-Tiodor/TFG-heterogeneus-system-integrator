from rest_framework.serializers import ModelSerializer

from heterogeneous_system_integrator.domain.mapping import Mapping


class MappingSerializer(ModelSerializer):
    
    class Meta:
        model = Mapping
        fields = '__all__'
