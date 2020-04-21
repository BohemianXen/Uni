from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from .models import *
from .forms import *
from django import forms
from .tasks import connect, check_status, update_action


def index(request):
    device = Device.objects.get(pk='C6:BC:91:2B:EB:A3')
    response = render(request, 'app/index.html', {})
    context = {'action': device.action.name}
    if request.is_ajax and request.method == 'GET' and request.GET.get('doUpdate') == 'true':
        check_status(device)
        context['status'] = Device.Status.labels[device.status]

        response = JsonResponse(context)
    elif request.is_ajax and request.method == 'POST' and request.POST.get('connect', '') == 'true':
        connect(device)  # TODO: This is blocking
        context['status'] = 'Connecting'  # Device.Status.labels[device.status],
        response = JsonResponse(context)
    else:
        pass

    return response
