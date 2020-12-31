from django.shortcuts import render

# Create your views here.
from .models import Accounts,MobileVerify,Order,Product
from django.http import HttpResponse
from django.http import JsonResponse
import json
import random
import string

random_str = lambda N: ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase)
                                                            for _ in range(N))
random_digi = lambda N: ''.join(random.SystemRandom().choice(string.digits) for _ in range(N))

def generate_digits():
    return str(random.randint(100000,1000000))

def index(request):

    #Accounts.objects.create(name="test name")
    return HttpResponse("hello niki junam...")


# def get_account(request):
#     our_accounts = Accounts.objects.all()
#     html_name = ""
#     for account in our_accounts:
#         print(account.name)
#         html_name += "<h3>" + account.name + "</h3>"
#     #Accounts.objects.create(name="test name")
#     return HttpResponse(html_name)

def get_account(request):
    our_accounts = Accounts.objects.all()
    accounts_list =[]
    for account in our_accounts:
        accounts_list += [
            {
                "name": account.name,
                "mobile": account.mobile,
                "password" : account.password,
            }
        ]

    content = {
        "status":"accountGOT",
        "accountsData": accounts_list
    }

    #Accounts.objects.create(name="test name")
    return JsonResponse(content)


def create_accounts(request):
    body = json.loads(request.body)
    name = body['name']
    mobile = body['mobile']
    password = body['password']
    if Accounts.objects.filter(mobile=mobile).exists():
        content = {
            "status": "your mobile is Exist.",
            "mobile" : mobile,
        }
    else:
        Accounts.objects.create(name=name,
                                mobile=mobile,
                                password=password)
        content = {
            "status": "your account created.",
            "name created" : name,

        }
        code = generate_digits()
        MobileVerify.objects.create(mobile=mobile,code=code)
        #TODO Create a function for sending sms api
        print("send sms code {} to mobile {}".format(code,mobile))
    return JsonResponse(content)


def mobile_verify(request):
    body = json.loads(request.body)
    mobile = body['mobile']
    code = body['code']
    if not MobileVerify.objects.filter(mobile=mobile).exists():
        content = {
            "status": "mobile not found!!!",
            "mobile" : mobile,
        }
    else:
        if MobileVerify.objects.filter(mobile=mobile).exists():
            this_mobile = MobileVerify.objects.filter(mobile=mobile).last()
            if this_mobile.code == code:
                Accounts.objects.filter(mobile=mobile).update(mobile_verify=True)
                MobileVerify.objects.filter(id=this_mobile.id).delete()
                content = {
                    "status": "mobili verified",
                    "mobile" : mobile,
                }
        else:
            content = {
                "status": "mobile not exists!!!",
                "mobile": mobile,
            }

    return JsonResponse(content)


def login(request):
    body = json.loads(request.body)
    mobile = body['mobile']
    password = body['password']
    if not Accounts.objects.filter(mobile=mobile).exists():
        content={
            "status":"there is no mobile",
            "mobile":mobile
        }

    else:
        this_account =  Accounts.objects.filter(mobile=mobile).get()
        if password == this_account.password:
            cookie = random_str(32)
            Accounts.objects.filter(mobile=mobile).update(cookie=cookie)
            content={
                "status":"you are login",
                "mobile":mobile,
                "cookie":cookie
            }
        else:
            content={
                "status":"wrong password",
                "mobile":mobile
            }

    return JsonResponse(content)


def edit_profile(request):
    body = json.loads(request.body)
    cookie = body['cookie']
    newpassword = body['newpassword']
    if not Accounts.objects.filter(cookie=cookie).exists():
        content={

            "status":"wrongcookie",
        }

    else:
        Accounts.objects.filter(cookie=cookie).update(password=newpassword)
        content={

            "status":"password changed.",
        }

    return JsonResponse(content)


def order(request):
    body = json.loads(request.body)
    cookie = body['cookie']
    product_list = body['Productlist']
    if not Accounts.objects.filter(cookie=cookie).exists():
        content={

            "status":"wrongcookie",
        }

    else:
        this_account = Accounts.objects.filter(cookie=cookie).get()
        this_order = Order.objects.create(account=this_account)
        total = 0
        for product_id in product_list:
            this_product = Product.objects.filter(id=product_id).get()
            this_price = this_product.price
            total += this_price
            this_order.products.add(this_product)
        this_order.total_price = total
        this_order.save()
        content={

            "status":"your order accepted.",
        }

    return JsonResponse(content)


def get_order(request):
    body = json.loads(request.body)
    cookie = body['cookie']
    order_id = body['orderid']
    if not Accounts.objects.filter(cookie=cookie).exists():
        content={

            "status":"wrongcookie",
        }

    else:
        this_order = Order.objects.filter(id=order_id).get()
        all_product = this_order.products.all()
        accountname = this_order.account
        li_pro = []
        for product in all_product:
            li_pro += [
                {
                    "title":product.product_title,
                    "price":product.price
                }
            ]
        content={

            "status":"order got.",
            "accountname":accountname.name,
            "product_list":li_pro
        }

    return JsonResponse(content)