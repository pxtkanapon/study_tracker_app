from django.urls import path
from .views import (
    TopicListCreateView, 
    TopicRetrieveUpdateDestroyView,
    LearningRecordListCreateView,
    LearningRecordRetrieveUpdateDestroyView,
)

urlpatterns = [
    # テーマに関するAPIエンドポイント
    # 例: GET /api/topics/, POST /api/topics/
    path('topics/', TopicListCreateView.as_view(), name='topic-list-create'),
    # 例: GET/PATCH/DELETE /api/topics/1/
    path('topics/<int:id>/', TopicRetrieveUpdateDestroyView.as_view(), name='topic-retrieve-update-destroy'),
    
    # 学習記録に関するAPIエンドポイント
    # 例: GET /api/records/, POST /api/records/
    path('records/', LearningRecordListCreateView.as_view(), name='record-list-create'),
    # 例: GET/PATCH/DELETE /api/records/1/
    path('records/<int:id>/', LearningRecordRetrieveUpdateDestroyView.as_view(), name='record-retrieve-update-destroy'),
]