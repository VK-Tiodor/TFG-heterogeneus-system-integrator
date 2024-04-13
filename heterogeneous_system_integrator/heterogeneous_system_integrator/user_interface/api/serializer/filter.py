from rest_framework.serializers import ModelSerializer

from heterogeneous_system_integrator.domain.filter import Filter


class FilterSerializer(ModelSerializer):
    
    class Meta:
        model = Filter
        fields = '__all__'
