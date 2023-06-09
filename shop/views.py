import json
from django.http import HttpResponse
from django.shortcuts import render
from .models import Orders, Product, OrderUpdate, Contact
from math import ceil

# Create your views here.


def index(request):
    allprods = []
    catProds = Product.objects.values("category", "product_id")
    cats = {item["category"] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = n//4 + ceil((n/4)-(n//4))
        allprods.append([prod, range(1, nslides), nslides])
    params = {"allprods": allprods}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone,desc=desc)
        contact.save()
        return render(request, 'shop/contact.html', {'added':True})
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request, "shop/tracker.html")


def search(request):
    return HttpResponse("We are at search")


def productView(request):
    return HttpResponse("We are at product view")


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('inputName', '')
        email = request.POST.get('inputEmail', '')
        address = request.POST.get('inputAddress', '') + " " + request.POST.get('inputAddress2', '')
        city = request.POST.get('inputCity', '')
        state = request.POST.get('inputState', '')
        pin = request.POST.get('inputZip', '')
        phone = request.POST.get('inputPhone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state, pin=pin, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="Your order was placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')


def thankYou(request):
    id = request.GET.get('id', '0')
    return render(request, 'shop/thankYou.html', {'id': id})
