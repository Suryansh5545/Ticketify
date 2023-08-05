from event.models import Event, SubEvent, Addon


def HandlePriceCalculation(request):
    event_id = request.data.get('event_id')
    selected_sub_events = request.data.get('selected_sub_events', []),
    selected_addons = request.data.get('selected_addons', [])
    total_sub_event_allowed = Event.objects.get(pk=event_id).sub_events_included_allowed
    sub_event_count = 0
    sub_event_price = 0
    addon_price = 0
    for sub_event in selected_sub_events[0]:
        if sub_event_count < total_sub_event_allowed:
            sub_event_count += 1
        else:
            sub_event_price += SubEvent.objects.get(pk=sub_event).price
    for addon in selected_addons:
        addon_price += Addon.objects.get(pk=addon).price
    event_price = Event.objects.get(pk=event_id).price
    total_price = event_price + sub_event_price + addon_price
    return int(total_price)