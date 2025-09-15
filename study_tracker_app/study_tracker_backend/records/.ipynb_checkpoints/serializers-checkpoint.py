# records/serializers.py
from rest_framework import serializers
from .models import LearningRecord, Topic

class TopicSerializer(serializers.ModelSerializer):
    """
    TopicモデルをJSONに変換するためのシリアライザ。
    """
    class Meta:
        model: type = Topic
        fields: str = '__all__'

class LearningRecordSerializer(serializers.ModelSerializer):
    """
    LearningRecordモデルをJSONに変換するためのシリアライザ。
    topicフィールドをIDで扱えるように修正。
    """
    topic = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(),
        help_text="学習テーマのID"
    )

    class Meta:
        model: type = LearningRecord
        fields: str = '__all__'