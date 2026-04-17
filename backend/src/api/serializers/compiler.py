from rest_framework import serializers
from src.core.models import TaskModel, SubmissionModel


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = [
            'id', 'title', 'description', 'starter_code',
            'difficulty', 'expected_output', 'created_at',
        ]
        # test_code is NOT exposed to the client


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = [
            'id', 'title', 'description', 'starter_code',
            'difficulty', 'expected_output', 'created_at',
        ]


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmissionModel
        fields = ['id', 'task', 'code', 'status', 'result', 'created_at']
        read_only_fields = ['status', 'result', 'created_at']
