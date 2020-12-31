from django.contrib import admin
from .models import Accounts,MobileVerify,Category,Product,Order

# Register your models here.

admin.site.register(Accounts)
admin.site.register(MobileVerify)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)