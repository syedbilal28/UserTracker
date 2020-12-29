from django.contrib import admin
from .models import Profile,Login,Company, Customer
# Register your models here.
class LoginIndicator (admin.TabularInline):
    model = Login

class CustomerAdmin(admin.ModelAdmin):
    inlines = [LoginIndicator]
    class Meta:
        model = Customer
admin.site.register(Company)
admin.site.register(Profile)
admin.site.register(Customer,CustomerAdmin)