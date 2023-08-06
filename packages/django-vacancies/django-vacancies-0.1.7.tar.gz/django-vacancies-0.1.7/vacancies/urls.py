from django.urls import path
from vacancies.views import VacancyDetailView, VacancyList

urlpatterns = [
    path('', VacancyList.as_view(), name='vacancy-index'),
    path('<slug:slug>/', VacancyDetailView.as_view(), name='vacancy-detail'),
]
