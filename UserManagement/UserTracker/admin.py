from django.contrib import admin
from .models import Profile,Login,Company, Website
# Register your models here.
class LoginIndicator (admin.TabularInline):
    model = Login

class ProfileAdmin(admin.ModelAdmin):
    inlines = [LoginIndicator]
    class Meta:
        model = Profile
admin.site.register(Company)
admin.site.register(Website)
admin.site.register(Profile,ProfileAdmin)