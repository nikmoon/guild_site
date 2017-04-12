
from django.views.generic.base import TemplateView, View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse

from .models import ChatMessage
from guild_site import settings
import json




class IndexView(TemplateView):

    template_name = 'chat/chat.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guild'] = settings.GUILD
        context['msgURL'] = settings.COMET_MSG_URL
        context['lastID'] = ChatMessage.objects.order_by('-id')[0].id
        return context



class MessageView(View):
    #
    #   POST - запись в базу нового сообщения
    #   GET - не разрешен
    #

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


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
    #   Возвращает последние сообщения:
    #   если задан параметр count - последние count сообщений;
    #   если задан параметр lastid - все сообщения с id > lastid
    #
    def get(self, request):
        if not request.user.is_authenticated():
            return JsonResponse({'error': 'Unknown user'}, status=403)

        count = request.GET.get('count')
        if count:
            try:
                count = int(count)
                return JsonResponse({
                    'messages': [msg.to_dict() for msg in ChatMessage.objects.order_by('-id')[:20]][::-1],
                    'username': request.user.username,
                })
            except ValueError:
                return JsonResponse({'error': 'Invalid count'}, status=400)
            except Exception:
                return JsonResponse({'error': 'Unknown error on JsonResponse with count parameter'}, status=400)


        lastID = request.GET.get('lastid')
        if lastID:
            try:
                lastID = int(lastID)
                return JsonResponse( {
                    'messages': [msg.to_dict() for msg in ChatMessage.objects.filter(id__gt=lastID).order_by('id')],
                    'username': request.user.username
                })
            except ValueError:
                return JsonResponse({'error': 'Invalid lastid'}, status=400)
            except Exception:
                return JsonResponse({'error': 'Unknown error on JsonResponse with lastid parameter'}, status=400)


        return JsonResponse({'error': 'Set count or lastid parameter'}, status=400)


