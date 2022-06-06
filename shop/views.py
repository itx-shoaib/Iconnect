import json

from django.shortcuts import render
from .models import Product , Contact , Orders , Orderupdate
from math import ceil

# Create your views here.
from django.http import HttpResponse

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank = False
    if request.method == "POST":
        # print(request)
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        # print(name,email,phone,desc)
        # contact first is the variable name or object of the class
        # Contact with capital C is the model name
        # name = name (firstname is the model field and the second name is the html id or class or name which is used to get POST request and noew its a varibale in the if statement
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html',{'thank':thank})

def tracker(request):
    # if request.method == "POST":
    #     # from orderupdate models and tracker form html
    #     orderId = request.POST.get('orderId', '')
    #     email = request.POST.get('email','')
    #     try:
    #         # we used filter tag in Order model and use saem technique as above
    #         order = Orders.objects.filter(order_id = orderId,email=email)
    #         if len(order)>0:
    #             # We use Order Update model and use it to publish order id
    #             update = Orderupdate.objects.filter(orderId = orderId)
    #             updates = [ ]
    #             for item in update:
    #                 updates.append({'text': item.update_desc, 'item': item.timestamp})
    #                 # We use json dump to covert python object into json objects
    #                 response = json.dumps(updates,default=str)
    #             return HttpResponse(response)
    #         else:
    #             return HttpResponse('{}')
    #     except Exception as e:
    #         return HttpResponse('{}')
    # return render(request, 'shop/tracker.html')

    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = Orderupdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({'status':'success','updates': updates,'itemsJson': order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitems"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')

# This function is for search button
def searchMatch(query,item):
    # Return true if item is available
    #We are adding .lower() after every model field  to make it case insensitive
    if query in item.desc.lower() or query in item.category.lower() or query in item.product_name.lower():
        return True
    else:
        return False

def search(request):
    # Query variable take request information from search button
    query = request.GET.get('search')
    # WE have copy the index code because in index all products are avalaible.
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query,item) ]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds , 'msg':' '}
    if len(allProds) == 0 or len(query) >4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)

def productsView(request,myid):
    product = Product.objects.filter(id=myid)

    return render(request, 'shop/prodView.html',{'product':product[0]})

def checkout(request):
    if request.method == "POST":
        # from order models and checkout form html
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('name','')
        amount = request.POST.get('amount','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        address = request.POST.get('address1','') + " " + request.POST.get('address12','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        # for order  ------ ( model field name = form html tag name or id )
        order = Orders(items_json= items_json, name=name,email=email, phone=phone ,address=address,city=city,state=state,zip_code=zip_code,amount = amount)
        order.save()
        # for order update
        update = Orderupdate(order_id = order.order_id , update_desc = "Your order has been place.")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank,'id':id})
    return render(request, 'shop/checkout.html')
