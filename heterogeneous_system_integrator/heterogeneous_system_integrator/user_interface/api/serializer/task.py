from rest_framework.serializers import ModelSerializer

from heterogeneous_system_integrator.domain.task import AsyncTask, PlannedTask, PeriodicTask


class AsyncTaskSerializer(ModelSerializer):
    
    class Meta:
        model = AsyncTask
        fields = '__all__'


class PlannedTaskSerializer(ModelSerializer):
    
    class Meta:
        model = PlannedTask
        fields = '__all__'


class PeriodicTaskSerializer(ModelSerializer):
    
    class Meta:
        model = PeriodicTask
        fields = '__all__'