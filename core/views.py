from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from core.models import Event, Location, Cart, Ticket
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
import json

def index(request):
    events = Event.objects.all()
    locations = Location.objects.all()

    context = {
        "events": events,
        "locations": locations
    }


    return render(request, 'core/index.html', context)

def event_detail_view(request, eid):
    event = get_object_or_404(Event, eid=eid)

    context = {
        "event": event
    }
    return render(request, 'core/event-detail.html', context)

def search_view(request):
    location = request.GET.get('location')  
    time = request.GET.get('time')      

    results = Event.objects.all()

    if location:
        results = results.filter(location__lid=location)  

    if time:
        try:
            start_date, end_date = time.split(" to ")
            results = results.filter(date__range=[start_date, end_date])
        except ValueError:
            pass  

    return render(request, 'core/search_results.html', {'results': results})

def cart_view(request):
    return render(request, 'core/cart.html')

def event_api(request, eid):
    event = get_object_or_404(Event, eid=eid)
    return JsonResponse({
        'id': event.eid,
        'title': event.title,
        'price': float(event.price),
        'image': event.image.url,
    })

def check_auth(request):
    return JsonResponse({
        'is_authenticated': request.user.is_authenticated
    })

@require_http_methods(["POST"])
def save_cart(request):
    try:
        data = json.loads(request.body)
        cart = data.get('cart', [])
        request.session['cart'] = cart
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required(login_url='userauth:login')
def payment_view(request):
    return render(request, 'core/payment.html')

@login_required(login_url='userauth:login')
def process_payment(request):
    if request.method == 'POST':
        return redirect('core:payment_success')
    
    return redirect('core:payment')

@login_required(login_url='userauth:login')
def payment_success_view(request):
    return render(request, 'core/payment_success.html')