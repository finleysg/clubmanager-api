import logging
from django.core.cache import cache
from register.models import RegistrationSlot

logger = logging.getLogger(__name__)


def load_cache(event_id):
    logger.info("Loading slot cache for event id {}".format(event_id))
    slots = dict()
    key = "event-{}".format(event_id)
    registrations = list(RegistrationSlot.objects.filter(event=event_id))
    for reg in registrations:
        slots[reg.id] = reg.status
    cache.set(key, slots, 60*60*60)
    return slots


def get_cache(event_id):
    key = "event-{}".format(event_id)
    slot_cache = cache.get(key)
    if slot_cache is None:
        slot_cache = load_cache(event_id)
    return slot_cache


def set_cache(event_id, slots):
    key = "event-{}".format(event_id)
    cache.set(key, slots, 60*60*60)


def can_reserve(event_id, slot_ids):
    result = True
    if slot_ids is not None:
        slots = get_cache(event_id)
        for slot_id in slot_ids:
            if slots[slot_id] != "A":
                result = False
    return result


def reserve_slots(event_id, slot_ids):
    if slot_ids is not None:
        slots = get_cache(event_id)
        for slot_id in slot_ids:
            slots[slot_id] = "X"  # pending or reserved doesn't matter -- both unavailable
        set_cache(event_id, slots)


def clear_slots(event_id, slot_ids):
    if slot_ids is not None:
        slots = get_cache(event_id)
        for slot_id in slot_ids:
            slots[slot_id] = "A"
        set_cache(event_id, slots)


def clear_slot(event_id, slot_id):
    slots = get_cache(event_id)
    slots[slot_id] = "A"
    set_cache(event_id, slots)
