from django.shortcuts import render
from .settings import GUILD

def index(request):
    return render(request, 'guild_site/index.html', {
        'guild': GUILD,
    })
