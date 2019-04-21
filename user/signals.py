from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from notifications.signals import notify
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def send_notification(sender, instance, **kwargs):
    # 注册成功,发送站内消息通知
    if kwargs['created'] == True:
        verb = '恭喜您注册成功,更多精彩内容等你发现'
        url = reverse('user_info')
        notify.send(instance, recipient=instance, verb=verb, url=url)

