
from django.views.generic.base import TemplateView
from guild_site.settings import GUILD


class ChatPageView(TemplateView):

    template_name = 'guild_site/chat.html'

    def get_context_data(self, **kwargs):
        context = super(ChatPageView, self).get_context_data(**kwargs)
        context['guild'] = GUILD
        return context


