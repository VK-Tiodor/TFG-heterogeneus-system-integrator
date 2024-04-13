from rest_framework.serializers import ModelSerializer

from heterogeneous_system_integrator.domain.subtask import Subtask


class SubtaskSerializer(ModelSerializer):
    
    class Meta:
        model = Subtask
        fields = '__all__'
        