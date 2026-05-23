from django.contrib import admin
from django.urls import path
from gestao.views import AlunoListView, fazer_chamada, registrar_presenca_iot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('alunos/', AlunoListView.as_view(), name='lista_alunos'),
    path('chamada/', fazer_chamada, name='fazer_chamada'), # Nossa rota nova
    path('api/iot/presenca/', registrar_presenca_iot, name='api_iot_presenca'),
]

