from django.shortcuts import render
from .models import NewsItem
from .settings import GUILD

def index(request):
    return render(request, 'guild_site/index.html', {
        'guild': GUILD,
        'news': NewsItem.objects.order_by('-id')[:5],
    })
