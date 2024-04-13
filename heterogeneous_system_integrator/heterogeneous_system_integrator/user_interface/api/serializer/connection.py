from rest_framework.serializers import ModelSerializer

from heterogeneous_system_integrator.domain.connection import Connection


class ConnectionSerializer(ModelSerializer):
    
    class Meta:
        model = Connection
        fields = '__all__'
