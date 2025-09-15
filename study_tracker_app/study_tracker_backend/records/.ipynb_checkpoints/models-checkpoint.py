# records/models.py
from django.db import models
from django.utils import timezone

class Topic(models.Model):
    """
    学習テーマを定義するモデル。
    """
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name = "学習テーマ"
        verbose_name_plural = "学習テーマ"

    def __str__(self):
        """
        オブジェクトの文字列表現を返します。
        """
        return self.title

class LearningRecord(models.Model):
    """
    個々の学習記録を定義するモデル。
    """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='records')
    date = models.DateField(default=timezone.now)
    # 実績時間（分）
    minutes = models.IntegerField(default=0)
    # 予定時間（分）
    planned_minutes = models.IntegerField(default=0)
    memo = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "学習記録"
        verbose_name_plural = "学習記録"
        ordering = ['-date'] # 日付の降順で並べ替え

    def __str__(self):
        """
        オブジェクトの文字列表現を返します。
        """
        return f'{self.topic.title} on {self.date}'