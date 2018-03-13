from django.contrib import admin
from verify_utils.models import CaptchaRecord, VerifyCodeRecord


# Register your models here.
class ShopUserAdmin(admin.ModelAdmin):
    fields = ['client_ip', 'captcha', 'encripted_captcha', 'created_at']

admin.site.register(CaptchaRecord, CaptchaRecordAdmin)


class VerifyCodeRecordAdmin(admin.ModelAdmin):
    fields = ['cell_phone', 'verify_code', 'verify_content', 'created_at']

admin.site.register(VerifyCodeRecord, VerifyCodeRecordAdmin)
