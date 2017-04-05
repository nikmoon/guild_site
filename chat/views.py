
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from guild_site.settings import GUILD


class ChatPageView(TemplateView):

    template_name = 'guild_site/chat.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ChatPageView, self).dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(ChatPageView, self).get_context_data(**kwargs)
        context['guild'] = GUILD
        return context


