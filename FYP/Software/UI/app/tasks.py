import asyncio
from celery import shared_task


@shared_task
def connect(device):
    """Background task when user clicks connect button. Starts connection manager in new thread."""

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.run_until_complete(device.cm.discover_devices())
    [device_name, device_id] = device.cm.find_detector()

    if device_id is not None:
        device.status = device.Status.CONNECTING
        if device_id != device.mac_address:
            device.mac_address = device_id  # TODO: Will fail if not unique (as intended) so try/catch
            if device.name != device_name:
                device.name = device_name
        device.save()

        print('\nConnecting to %s (with address %s)' % (device.cm.target_name, device.cm.target_address))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(device.cm.connect(loop))
    else:
        print('Could not find a fall detector device')
        device.status = device.Status.DISCONNECTED

    check_status(device)


@shared_task
def check_status(device):
    """Check BLE device status and update entry for given device to match this."""

    if device.cm.connected:
        if device.cm.streaming:
            device.status = device.Status.STREAMING
            update_action(device)
        else:
            device.status = device.Status.CONNECTED
    else:
        device.status = device.Status.DISCONNECTED
    device.save()


@shared_task
def update_action(device):
    """Check device prediction and update table entry for given device to reflect this if it has changed."""

    if device.cm.streaming:
        new_action = device.cm.action
        if new_action != device.action_id:
            device.action_id = new_action
            device.save()
