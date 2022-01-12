from django.views.generic import *
from django.urls import reverse
from .models import *
from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin

# 討論主題列表
class TopicList(ListView):
    model = Topic
    ordering = ['-created']
    paginate_by = 20        # 每頁主題數

# 新增討論主題
class TopicNew(CreateView):
    model = Topic
    fields = ['subject', 'content']

    def get_success_url(self):
        return reverse('topic_list')

    def form_valid(self, form):
        # 自動將目前使用者填入討論主題的作者欄
        form.instance.author = self.request.user
        return super().form_valid(form)

# 檢視討論主題
class TopicView(DetailView):
    model = Topic

    def get_object(self):
        topic = super().get_object()    # 取得欲查看的討論主題
        topic.hits += 1     # 等同 topic.hits = topic.hits + 1
        topic.save()
        return topic

# 刪除討論主題
class TopicDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'topic.delete_topic'
    model = Topic
    template_name = 'confirm_delete.html'
    pk_url_kwarg = 'tid'

    def get_success_url(self):
        return reverse('topic_list')

# 回覆討論主題
class TopicReply(CreateView):
    model = Reply
    fields = ['content']
    template_name = 'topic/topic_form.html'

    def form_valid(self, form):
        topic = Topic.objects.get(id=self.kwargs['tid'])
        form.instance.topic = topic
        form.instance.author = self.request.user
        topic.replied = datetime.now()  # 更新討論主題回覆時間
        topic.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('topic_view', args=[self.kwargs['tid']])

# 刪除討論回覆
class ReplyDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'topic.delete_reply'
    model = Reply
    template_name = 'confirm_delete.html'

    def get_success_url(self):
        reply = self.get_object()   # 取得欲刪除的那筆紀錄
        return reverse('topic_view', args=[reply.topic.id])