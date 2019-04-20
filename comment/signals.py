import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import send_mail
# from BlogProject import settings
from django.conf import settings
from .models import Comment

@receiver(post_save, sender=Comment)
def send_notification(sender, instance, **kwargs):
    # 发送站内消息通知
    if instance.reply_to is None:
        # 评论通知
        recipient = instance.content_object.get_user()
        if instance.content_type.model == 'blog':
            verb = '%s评论了你的博客《%s》' % (instance.user.get_nickname_or_username(), instance.content_object.title)
        else:
            raise Exception('unkown comment object type')
    else:
        # 回复通知
        recipient = instance.reply_to
        verb = '%s回复了你的评论"%s"' % (instance.user.get_nickname_or_username(), strip_tags(instance.parent.text))
    url = instance.content_object.get_url() + '#comment_' + str(instance.id)
    notify.send(instance.user, recipient=recipient, verb=verb, url=url)

class SendEmail(threading.Thread):
    def __init__(self, subject, message, from_email, email, fail_silently=False):
        self.subject = subject
        self.message = message
        self.from_email = from_email
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)
    def run(self):
        send_mail(self.subject, '', self.from_email, [self.email], fail_silently = self.fail_silently, html_message=self.message)

@receiver(post_save, sender=Comment)
def send_email(sender, instance, **kwargs):
    # 发送邮件通知
    if instance.parent is None:
        ##有人评论我的博客
        subject = '有人评论你的博客'
        email = instance.content_object.get_email()
    else:
        # 有人回复我的评论
        subject = '有人回复你的评论'
        email = instance.reply_to.email
    if email != '':
        content = {}
        content['content_text'] = instance.text
        content['url'] = instance.content_object.get_url()
        # message = '%s<a href="%s">点击查看</a>' % (self.text, self.content_object.get_url())
        message = render_to_string('comment/send_email_content.html', content)
        from_email = settings.EMAIL_HOST_USER
        send_mail = SendEmail(subject, message, from_email, email)
        send_mail.start()