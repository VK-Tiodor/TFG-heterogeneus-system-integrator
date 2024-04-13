from rest_framework.serializers import ModelSerializer

from heterogeneous_system_integrator.domain.task import Task


class TaskSerializer(ModelSerializer):
    
    class Meta:
        model = Task
        fields = '__all__'
        