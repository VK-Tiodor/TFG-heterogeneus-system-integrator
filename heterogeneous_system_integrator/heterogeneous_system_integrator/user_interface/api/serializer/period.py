from rest_framework.serializers import ModelSerializer

from heterogeneous_system_integrator.domain.period import Period


class PeriodSerializer(ModelSerializer):
    
    class Meta:
        model = Period
        fields = '__all__'
        exclude = ['celery_crontab']
