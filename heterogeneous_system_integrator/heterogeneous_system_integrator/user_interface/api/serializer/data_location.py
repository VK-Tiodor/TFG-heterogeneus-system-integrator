from rest_framework.serializers import ModelSerializer

from heterogeneous_system_integrator.domain.data_location import ApiDataLocation, DbDataLocation, FtpDataLocation


class ApiDataLocationSerializer(ModelSerializer):
    
    class Meta:
        model = ApiDataLocation
        fields = '__all__'


class DbDataLocationSerializer(ModelSerializer):
    
    class Meta:
        model = DbDataLocation
        fields = '__all__'


class FtpDataLocationSerializer(ModelSerializer):
    
    class Meta:
        model = FtpDataLocation
        fields = '__all__'
