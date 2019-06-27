from rest_framework import serializers
from . import models
import json, os
from TakeTest import settings
from datetime import datetime, timedelta
from . import utils
from django.urls import reverse



class TestsSerializer(serializers.ModelSerializer):
    test_content = serializers.SerializerMethodField()
    class Meta:
        model = models.Tests
        fields = ('test_name', 'test_file', 'author', 'test_content', 'start_date', 'duration', 'end_date', 'is_active', 'exam_duration')
        read_only_fields = ['author', 'test_content', 'end_date', 'is_active']

    def create(self, validated_data):
        return models.Tests.objects.create(**validated_data)

    def validate_test_file(self, test_file):
        try:
            is_valid_test_file = json.loads(test_file.read())
        except ValueError as e:
            raise serializers.ValidationError("Invalid Test File uploaded")
        return test_file

    def get_test_content(self, obj):
        if obj.test_file:
            file_path = os.path.join(settings.MEDIA_ROOT, str(obj.test_file))
            with open(file_path) as test_file:
                return json.loads(test_file.read())

    def update(self, instance, validated_data):
        # print (instance.test_id)
        instance.start_date = validated_data['start_date']
        instance.duration = validated_data['duration']
        instance.exam_duration = validated_data['exam_duration']
        instance.end_date = instance.start_date + timedelta(hours=instance.duration)
        instance.is_active = True
        # print (reverse('TakeTestApp:taketest'))
        # instance.url = reverse('TakeTestApp:taketest')
        instance.save()
        return instance


class ReadyToAttendSerializer(serializers.ModelSerializer):
    test_content = serializers.SerializerMethodField()
    class Meta:
        model = models.Tests
        fields = ('id', 'test_name', 'test_file', 'author', 'test_content', 'start_date', 'duration', 'end_date', 'is_active')
        read_only_fields = ['id', 'author', 'test_content', 'start_date', 'end_date', 'is_active']

    def get_test_content(self, obj):
        if obj.test_file:
            file_path = os.path.join(settings.MEDIA_ROOT, str(obj.test_file))
            with open(file_path) as test_file:
                return json.loads(test_file.read())


class TakeTestSerializer(serializers.ModelSerializer):
    test_content = serializers.SerializerMethodField()

    class Meta:
        model = models.Tests
        fields = ('id', 'test_name', 'test_file', 'test_content', 'start_date', 'end_date', 'exam_duration')
        read_only_fields = ['id', 'test_name', 'test_file', 'test_content', 'start_date', 'end_date', 'exam_duration']

    def get_test_content(self, obj):
        if obj.test_file:
            file_path = os.path.join(settings.MEDIA_ROOT, str(obj.test_file))
            with open(file_path) as test_file:
                return json.loads(test_file.read())


class PostAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Results
        fields = ('test', 'user', 'answers')
        read_only_fields = ['user', 'score']

    def create(self, validated_data):
        score = utils.BackendOperations().calculate_score(
            validated_data['answers'],
            validated_data['test'])
        validated_data['score'] = score
        return models.Results.objects.create(**validated_data)





