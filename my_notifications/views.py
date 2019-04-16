from django.shortcuts import render,redirect,get_object_or_404
from notifications.models import Notification
from django.urls import reverse
# Create your views here.
def my_notifications(request):
    content = {}
    return render(request, 'my_notifications/my_notifications.html', content)
def my_notification(request, my_notification_id):
    notification = get_object_or_404(Notification, id=my_notification_id)
    notification.unread = False
    notification.save()
    return redirect(notification.data['url'])
def delete_my_read_notifications(request):
    notifications = request.user.notifications.read()
    notifications.delete()
    return redirect(reverse('my_notifications'))