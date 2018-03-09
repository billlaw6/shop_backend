import hashlib
import json
import base64
import io
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from utils.captcha import SimpleCaptcha


# Create your views here.
@require_http_methods(["GET", "POST"])
def get_captcha(request):
    """
    返回验证码及验证码的MD5加密结果 length = 4 width = 100 height = 40 fontsize = 36 接收上述参数
    """
    captcha_para = {'length':4, 'width':100, 'height':40, 'fontsize': 36}
    if request.method == 'POST':
        paras = json.loads(request.body.decode())
        captcha_para = default_para.update(paras)
    else:
        print(captcha_para)

    sc = SimpleCaptcha(length=captcha_para['length'],
        size=(captcha_para['width'], captcha_para['height']),
        fontsize=captcha_para['fontsize'],
        random_text=True, random_bgcolor=True)
    img, text = sc.get_captcha()
    md = hashlib.md5()
    # str->bytes: encode编码
    md.update(text.encode('utf8'))
    # print(md.hexdigest())
    # buffer = io.StringIO()
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    # print(base64.b64encode(buffer.getvalue()).decode())
    rsp = {}
    rsp['code'] = md.hexdigest()
    # bytes->str: decode解码
    rsp['img'] = base64.b64encode(buffer.getvalue()).decode()
    return HttpResponse(json.dumps(rsp))


