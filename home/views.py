# importing from python library
import uuid
import json
import requests

# importing from django library
from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.views.generic import View
from django.db.models import Q
from django.core.paginator import Paginator

from . forms import *
from . models import *

# Create your views here.

def index(request):
    latest = Product.objects.filter(latest=True)
    trending = Product.objects.filter(trending=True)
    team = Team.objects.all()[:3]

    
    context = {
        'vic':latest,
        'math':trending,
        'team':team,
    }
    return render(request, 'index.html', context)

    # return HttpResponse('Hello there gladly welcom me to django!')

def contact(request):
    form = ContactForm()# instantiate the contactform for a GET request
    if request.method == 'POST': # make a POST request
        form = ContactForm(request.POST)#instantiate the contactform for a POST request
        if form.is_valid(): # Django will test to validate the form
           form.save() # if valid, save the data to the DataBase
           messages.success(request, 'message sent successfully!')
           return redirect('index')#  return to index once the post action is carried out   
    return render(request, 'index.html')
    # return HttpResponse('Contact done')


def products(request):
    product = Product.objects.all()
    goods = Paginator(product, 4)
    mygoods = request.GET.get('page')
    mygoods_good = goods.get_page(mygoods)
    
    context = {
        'mygoods_good':mygoods_good,
    }
    return render(request, 'products.html',context)

def details(request, id):
    # detail = Prouct.objects.get(id=id)
    detail = Product.objects.get(pk=id)

    context = {
        'detail':detail,
    }
    
    return render(request, 'details.html',context)
# authentication

def signout(request):
    logout(request)
    return redirect('signin')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwrodd = request.POST['password']
        user = authenticate(request,username= username, password=passwrodd)
        if user is not None:
            login(request, user)
            messages.success(request, 'Signin Successful!')
            return redirect('index')
        else:
            messages.error(request, 'Username/Password incorrect. Kindly supply valid details')
            return redirect('signin')
    return render(request, 'signin.html')

def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        # today
        phone = request.POST['phone']
        address = request.POST['address']
        state = request.POST['state']
        pix = request.POST['pix']
        form = SignupForm(request.POST)
        # today
        if form.is_valid():
            newuser = form.save()
            # today
            newprofile = Profile(user= newuser)
            newprofile.first_name = newuser.first_name
            newprofile.last_name = newuser.last_name
            newprofile.email = newuser.email
            newprofile.phone = phone
            newprofile.address = address
            newprofile.state = state
            newprofile.pix = pix
            newprofile.save()
            login(request, newuser)# today
            messages.success(request, 'Signup successful!')
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return redirect('signup')
    return render(request,'signup.html')
# authentication done

# profile
@login_required(login_url='signin')
def profile(request):
    profile = Profile.objects.get(user__username = request.user.username)
    # profile = Profile.objects.get(user_id = request.user.username)

    context = {
        'profile':profile,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def profile_update(request):
    profile = Profile.objects.get(user__username = request.user.username)
    update = ProfileUpdate(instance = request.user.profile)    #instantiate the update for a get request along with the user's details 
    if request.method == 'POST':
        update = ProfileUpdate(request.POST, request.FILES, instance = request.user.profile)
        if update.is_valid():
            update.save()
            messages.success(request, 'Profile update Successful!')
            return redirect('profile')
        else:
            messages.error(request, update.errors)
            return redirect('profle_update')
    context = {
        'profile':profile,
        'update':update,
    }
    return render(request, 'profile_update.html', context)
# profile done

@login_required(login_url='signin')
def password(request):
    profile = Profile.objects.get(user__username = request.user.username)
    form = PasswordChangeForm(request.user)
    # form = PasswordChangeForm()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        # form = PasswordChangeForm(request.user)
        # form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'password change successfull!')
            return redirect('profile')
        else:
            messages.error(request, form.errors)
            return redirect('password')

    context = {
        'form':form,
        'profile':profile,
    }
    return render(request, 'password.html', context)


def search(request):
    if request.method == 'POST':
        items = request.POST['search']
        #Q is a function from django library
        # for the tag field searched
        # searched = Q(Q(leather__icontains=items)| (Q(name__icontains=items)) |(Q(name__icontains=items)))
        searched = Q((Q(name__icontains=items)) |(Q(price__icontains=items)))
        searched_item = Product.objects.filter(searched)

        context = {
            'items':items,
            'searched_item':searched_item,
        }
        
        return render(request, 'search.html', context)
    else:
        return render(request, 'search.html')


# shopcart
def shopcart(request):
    if request.method == 'POST':
        quant = int(request.POST['quantity'])
        item_id = request.POST['product_id']
        product = Product.objects.get(pk=item_id)
        order_num = Profile.objects.get(user__username = request.user.username)
        cart_no = order_num.id

        cart = Shopcart.objects.filter(user__username = request.user.username, paid= False) #Shopper with unpaid items 
        if cart:        # existing order(object) with a selected product quantity to be incermented/ Shopcart with a select product(s)
            basket = Shopcart.objects.filter(product_id=product.id, user__username=request.user.username).first()       # user already picked an product
            if basket:
                basket.quantity += quant #for increment of the product for the same user
                basket.amount = product.price * quant
                basket.save()
                messages.success(request, 'Item  added to cart')
                return redirect('products')
            else:
                newitem = Shopcart()
                newitem.user = request.user
                newitem.product = product
                newitem.quantity = quant
                newitem.price = product.price
                newitem.name_id = product.name
                newitem.amount = product.price * quant
                newitem.order_no = cart_no
                newitem.paid = False
                newitem.save()
                messages.success(request, 'product added')
                return redirect('products')
        else:
            newcart = Shopcart()    #create an order for teh first time 
            newcart.user = request.user
            newcart.product = product
            newcart.quantity = quant
            newcart.price = product.price
            newcart.name_id = product.name
            newcart.amount = product.price * quant
            newcart.order_no = cart_no
            newcart.paid = False
            newcart.save()
            messages.success(request, 'product added to shopcart!')
            return redirect('products')
    return redirect('products')


def displaycart(request):
    trolley = Shopcart.objects.filter(user__username =request.user.username, paid=False)
    profile = Profile.objects.get(user__username = request.user.username)


    # initializing
    subtotal = 0
    vat = 0
    total = 0

    for cart in trolley:
        subtotal += cart.price * cart.quantity

    vat = 0.075 * subtotal

    total = vat + subtotal

    context = {
        'trolley':trolley,
        'profile':profile,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
    }
    
    return render(request, 'displaycart.html', context)
# shopcart done

def deleteitem(request):
    item_id = request.POST['item_id']
    item_delete = Shopcart.objects.get(pk=item_id)
    item_delete.delete()
    messages.success(request, 'item deleted successfully.')
    return redirect('displaycart')

def increase(request):
    if request.method == 'POST':
        the_item = request.POST['itemid']
        the_quant = int(request.POST['quant'])
        modify = Shopcart.objects.get(pk=the_item)
        modify.quantity += the_quant
        modify.amount = modify.price * modify.quantity
        modify.save()
    return redirect('displaycart')

# checkout using class based view and axios get request
class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        summary = Shopcart.objects.filter(user__username = request.user.username, paid= False)

        subtotal = 0
        vat = 0
        total = 0

        for cart in summary:
            subtotal += cart.price * cart.quantity

        vat = 0.075 * subtotal

        total = vat + subtotal

        context ={
            'summary':summary,
            'total':total,
        }

        return render(request, 'checkout.html', context)
# checkout using class based view and axios get request done



def pay(request):
    if request.method == 'POST':
        # collecting data to send out to paystack
        api_key = 'sk_test_43762140e809dbc5ffee4d9c1e84d8c72afd6b9d'
        curl = 'https://api.paystack.co/transaction/initialize'
        # cburl = 'http://54.198.194.99/callback'
        cburl = 'http://127.0.0.1:7000/callback'
        user = User.objects.get(username = request.user.username)
        email = user.email
        total = float(request.POST['total']) * 100
        cart_no = user.profile.id
        transac_code = str(uuid.uuid4())
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference':transac_code,'email':email, 'amount':int(total), 'order_number':cart_no, 'callback_url':cburl, 'currency': 'NGN'}
        # print('TESTING', data)
        # integrating to paystack
        try:
            r = requests.post(curl, headers= headers, json= data)
        except Exception:
            messages.error(request, 'Network busy, refresh and try again')
        else:
            transback = json.loads(r.text)
            rdurl = transback['data']['authorization_url']
            return redirect(rdurl)
        return redirect('displaycart')



def callback(request):
    profile = Profile.objects.get(user__username = request.user.username)
    basket = Shopcart.objects.filter(user__username = request.user.username, paid=False)
    # pay = Payment.objects.get(user__username = request.user.username, paid=True)

    for item in basket:
        item.paid = True 
        item.save()

        stock = Product.objects.get(pk= item.product.id)
        stock.max_quantity -= item.quantity 
        stock.save()

    context = {
        'profile':profile,
    }
    return render(request, 'callback.html', context)



@login_required(login_url='signin')
def history(request):
    profile = Profile.objects.get(user__username = request.user.username)
    basket = Shopcart.objects.filter(user__username = request.user.username, paid=True)


    context = {
        'profile':profile,
        'basket':basket,
    }
    return render(request, 'history.html', context)












































































# def contact(request):
#     form = ContactForm()
#     if request.method == 'POST':
#         form = ContactForm(request, POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'message sent successsfully!')
#             return redirect('index')
#         else:
#             messages.errors(request.forms.errors)
#             return redirect('contact')
#     return render(request, 'index.html')