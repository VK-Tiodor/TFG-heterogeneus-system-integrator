from rest_framework.serializers import ModelSerializer

from heterogeneous_system_integrator.domain.path import ApiPath, DbPath, FtpPath


class ApiPathSerializer(ModelSerializer):
    
    class Meta:
        model = ApiPath
        fields = '__all__'


class DbPathSerializer(ModelSerializer):
    
    class Meta:
        model = DbPath
        fields = '__all__'


class FtpPathSerializer(ModelSerializer):
    
    class Meta:
        model = FtpPath
        fields = '__all__'
