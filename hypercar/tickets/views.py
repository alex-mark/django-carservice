from django.views import View
from django.views.generic.base import TemplateView
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import tickets, get_minutes, get_next, pop_next


class MainView(View):
    def get(self, request, *args, **kwargs):
        menu = [
            {'link': 'change_oil', 'text': 'Change Oil'},
            {'link': 'inflate_tires', 'text': 'Inflate Tires'},
            {'link': 'diagnostic', 'text': 'Diagnostic'},
        ]
        return render(request, 'tickets/main.html', context={'menu': menu})


class GetTicketView(TemplateView):
    template_name = 'tickets/get_ticket.html'

    def get_context_data(self, **kwargs):
        operation = self.kwargs['operation']

        number = max(max(car_numbers) if car_numbers else 0 for car_numbers in tickets.values()) + 1
        minutes_to_wait = get_minutes(operation)
        if operation == 'change_oil':
            tickets['change_oil'].append(number)
        elif operation == 'inflate_tires':
            tickets['inflate_tires'].append(number)
        elif operation == 'diagnostic':
            tickets['diagnostic'].append(number)

        return {'number': number, 'minutes_to_wait': minutes_to_wait}


class ProcessingView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'n_change_oil': len(tickets['change_oil']),
            'n_inflate_tires': len(tickets['inflate_tires']),
            'n_diagnostic': len(tickets['diagnostic'])
        }
        return render(request, 'tickets/processing.html', context=context)

    def post(self, request, *args, **kwargs):
        pop_next()
        return redirect('/processing')


class NextView(TemplateView):
    template_name = 'tickets/next.html'

    def get_context_data(self, **kwargs):
        return {'next_number': get_next()}