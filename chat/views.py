
from django.views.generic.base import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from .models import ChatMessage
from guild_site import settings
from guild_site.views import MySecretView
import json


def get_last_messages(count):
    return list(ChatMessage.objects.order_by('id'))[-count:]


class ChatPageView(TemplateView):

    template_name = 'chat/chat.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ChatPageView, self).dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(ChatPageView, self).get_context_data(**kwargs)
        context['guild'] = settings.GUILD
        context['msg_url_post'] = reverse('message')
        context['msg_url_get'] = settings.COMET_URL_MESSAGE
        context['last_messages'] = get_last_messages(5)
        context['last_id'] = context['last_messages'][-1].id
        return context



class MessageView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(MessageView, self).dispatch(*args, **kwargs)


    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('Вам сюда нельзя', status=401)

        newMessage = ChatMessage.objects.create(msgText=request.body, msgAuthor=request.user)
        return HttpResponse('Its OK')


class LatestMessagesView(MySecretView):

    def get(self, request):
        try:
            count = int(request.GET.get('count'))
            if count < 1:
                raise Exception()
        except:
            return HttpResponse('Ошибка в параметре count', status=500)
            
        latestMessages = [msg.to_dict() for msg in get_last_messages(int(count))]
        return HttpResponse(json.dumps(latestMessages))



class LastIDView(MySecretView):

    def get(self, request):
        return HttpResponse(ChatMessage.objects.latest('id').id)
        #if request.body:
        #    data = json.loads(request.body.decode('utf-8'))
        #    if 'secret' in data and data['secret'] == settings.SECRET_KEY:
        #        return HttpResponse(ChatMessage.objects.latest('id').id)
        
        #return HttpResponse('Вам сюда нельзя', status=401)




