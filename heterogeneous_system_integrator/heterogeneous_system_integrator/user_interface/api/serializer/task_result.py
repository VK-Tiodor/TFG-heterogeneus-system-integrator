from rest_framework.serializers import ModelSerializer
from django_celery_results.models import TaskResult


class TaskResultSerializer(ModelSerializer):
    
    class Meta:
        model = TaskResult
        fields = '__all__'
