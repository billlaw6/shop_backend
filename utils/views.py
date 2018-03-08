import hashlib
import json
import base64
import io
from django.http import HttpResponse

from utils.captcha import SimpleCaptcha

# Create your views here.
def get_captcha(request):
    """
    返回验证码及验证码的MD5加密结果
    """
    sc = SimpleCaptcha(length=7, fontsize=36, random_text=True, random_bgcolor=True)
    img, text = sc.get_captcha()
    md = hashlib.md5()
    md.update(text)
    print(md.hexdigest())

    buffer = io.StringIO()
    img.save(buffer, format='JPEG')
    print(base64.b64encode(buffer.getvalue()))
    return HttpResponse('captcha')


