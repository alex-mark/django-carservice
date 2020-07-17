from collections import deque
from django.db import models

CHANGE_OIL_MINUTES = 2
INFLATE_TIRES_MINUTES = 5
DIAGNOSTIC_MINUTES = 30

tickets = {
    'change_oil': deque(),
    'inflate_tires': deque(),
    'diagnostic': deque()
}

next_num = None


def get_minutes(operation):
    minutes = 0

    if operation == 'change_oil':
        minutes = len(tickets['change_oil']) * CHANGE_OIL_MINUTES
    elif operation == 'inflate_tires':
        minutes = len(tickets['change_oil']) * CHANGE_OIL_MINUTES \
                  + len(tickets['inflate_tires']) * INFLATE_TIRES_MINUTES
    elif operation == 'diagnostic':
        minutes = len(tickets['change_oil']) * CHANGE_OIL_MINUTES \
                  + len(tickets['inflate_tires']) * INFLATE_TIRES_MINUTES \
                  + len(tickets['diagnostic']) * DIAGNOSTIC_MINUTES
    return minutes


def get_next():
    return next_num

def pop_next():
    global next_num
    if tickets['change_oil']:
        next_num = tickets['change_oil'].popleft()
    elif tickets['inflate_tires']:
        next_num = tickets['inflate_tires'].popleft()
    elif tickets['diagnostic']:
        next_num = tickets['diagnostic'].popleft()
