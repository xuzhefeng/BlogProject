
from django.urls import path,include
from . import views
urlpatterns = [

    path('', views.my_notifications, name='my_notifications'),
    path('<int:my_notification_id>', views.my_notification, name='my_notification'),
    path('delete_my_read_notifications', views.delete_my_read_notifications, name='delete_my_read_notifications'),
]
