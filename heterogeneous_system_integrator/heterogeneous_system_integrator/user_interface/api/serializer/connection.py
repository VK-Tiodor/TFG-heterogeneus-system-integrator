from rest_framework.serializers import ModelSerializer

from heterogeneous_system_integrator.domain.connection import ApiConnection, DbConnection, FtpConnection


class ApiConnectionSerializer(ModelSerializer):
    
    class Meta:
        model = ApiConnection
        fields = '__all__'


class DbConnectionSerializer(ModelSerializer):
    
    class Meta:
        model = DbConnection
        fields = '__all__'


class FtpConnectionSerializer(ModelSerializer):
    
    class Meta:
        model = FtpConnection
        fields = '__all__'
