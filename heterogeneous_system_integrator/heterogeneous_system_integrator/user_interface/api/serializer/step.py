from rest_framework.serializers import ModelSerializer

from heterogeneous_system_integrator.domain.step import TransferStep, TransformStep


class TransferStepSerializer(ModelSerializer):
    
    class Meta:
        model = TransferStep
        fields = '__all__'


class TransformStepSerializer(ModelSerializer):
    
    class Meta:
        model = TransformStep
        fields = '__all__'
