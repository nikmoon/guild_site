
from django.views.generic.base import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from .models import ChatMessage
from guild_site import settings
from guild_site.views import SecretView
import json




class ChatPageView(TemplateView):

    template_name = 'chat/chat.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ChatPageView, self).dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(ChatPageView, self).get_context_data(**kwargs)
        context['guild'] = settings.GUILD
        context['msgURL'] = settings.COMET_MSG_URL
        context['lastMessages'] = [msg for msg in ChatMessage.objects.order_by('-id')[:20]][::-1]
        context['lastID'] = context['lastMessages'][-1].id
        return context



class MessageView(View):
    #
    #   POST - запись в базу нового сообщения
    #   GET - не разрешен
    #

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(MessageView, self).dispatch(*args, **kwargs)

    def post(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({'error': 'Unknown user'}, status=403)

        newMessage = ChatMessage.objects.create(msgText=request.body, msgAuthor=request.user)
        return JsonResponse({
            'username': request.user.username,
            'messages': [newMessage.to_dict()],
        })


class LatestMessagesView(View):
    #
    #   Возвращает сообщения после id = lastid
    #
    def get(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({'error': 'Unknown user'}, status=403)

        try:
            lastID = int(request.GET.get('lastid'))
            if lastID < 1:
                raise Exception()
        except:
            return JsonResponse({'error': 'Invalid lastid'}, status=400)
 
        data = {
            'messages': [msg.to_dict() for msg in ChatMessage.objects.filter(id__gt=lastID).order_by('id')],
            'username': request.user.username
        }
        return JsonResponse(data)



