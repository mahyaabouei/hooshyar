from django.urls import path
from .views import SelectTimeUserViewset ,SetTimeConsultant , SelectTimeConsultantViewset

urlpatterns = [
    path('selecttime/<int:pk>/', SelectTimeUserViewset.as_view(), name='select-time'),
    path('selecttime/consultant/', SelectTimeConsultantViewset.as_view(), name='select-time-consultant'),
    path('settime/consultant/', SetTimeConsultant.as_view(), name='set-time-consultant'),
    path('delete/settime/', SetTimeConsultant.as_view(), name='set_time_delete'),

]


