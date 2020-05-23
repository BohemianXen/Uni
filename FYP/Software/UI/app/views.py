from django.shortcuts import render
from django.http import JsonResponse
from .models import Device
from .tasks import connect, check_status


def index(request):
    """Handles demo app page requests."""

    device = Device.objects.get(pk='C6:BC:91:2B:EB:A3')  # TODO: Get this through user details after adding login page
    response = render(request, 'app/index.html', {})
    context = {'action': device.action.name}

    if request.is_ajax and request.method == 'GET' and request.GET.get('doUpdate') == 'true':  # Refresh labels
        check_status(device)
        context['status'] = Device.Status.labels[device.status]
        response = JsonResponse(context)
    elif request.is_ajax and request.method == 'POST' and request.POST.get('connect', '') == 'true':  # Connect
        connect(device)
        context['status'] = 'Connecting'  # Device.Status.labels[device.status]
        response = JsonResponse(context)
    else:
        pass

    return response
