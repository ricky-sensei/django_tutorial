from django.contrib import admin

# quiestionモデルをインポート
from .models import Question

# モデルをadmin管理画面に登録
admin.site.register(Question)


