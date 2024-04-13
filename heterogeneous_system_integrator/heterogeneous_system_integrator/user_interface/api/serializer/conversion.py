from rest_framework.serializers import ModelSerializer

from heterogeneous_system_integrator.domain.conversion import Conversion


class ConversionSerializer(ModelSerializer):
    
    class Meta:
        model = Conversion
        fields = '__all__'
