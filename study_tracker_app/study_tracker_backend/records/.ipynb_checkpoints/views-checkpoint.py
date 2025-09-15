from rest_framework import generics
from .models import Topic, LearningRecord
from .serializers import TopicSerializer, LearningRecordSerializer

class TopicListCreateView(generics.ListCreateAPIView):
    """
    GET: テーマのリストを取得します。
    POST: 新しいテーマを作成します。
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class TopicRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: 特定のIDを持つテーマの詳細を取得します。
    PATCH: 特定のIDを持つテーマを部分的に更新します。
    DELETE: 特定のIDを持つテーマを削除します。
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    lookup_field = 'id'

class LearningRecordListCreateView(generics.ListCreateAPIView):
    """
    GET: 学習記録のリストを取得します。
    POST: 新しい学習記録を作成します。
    """
    queryset = LearningRecord.objects.all()
    serializer_class = LearningRecordSerializer

class LearningRecordRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: 特定のIDを持つ学習記録の詳細を取得します。
    PATCH: 特定のIDを持つ学習記録を部分的に更新します。
    DELETE: 特定のIDを持つ学習記録を削除します。
    """
    queryset = LearningRecord.objects.all()
    serializer_class = LearningRecordSerializer
    lookup_field = 'id'