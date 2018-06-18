#!/usr/bin/env python
#-*-coding=utf-8-*-
#
#File Name: ".expand("%"))
#Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
#Author LiuBin on: 2018-03-07 20:47
# 源自 Python数据可视化编程实战
#


from PIL import Image, ImageDraw, ImageFont
import random
import string


class SimpleCaptchaException(Exception):
    pass


class SimpleCaptcha(object):
    """
    返回Image对象和对应的内容
    """
    def __init__(self, length=5, size=(200, 100), fontsize=36, random_text=None, random_bgcolor=None):
        self.size = size
        self.text = 'CAPTCHA'
        self.fontsize = fontsize
        self.bgcolor = 255
        self.length = length
        # current captcha image
        self.image = None

        if random_text:
            self.text = self._random_text()

        if not self.text:
            raise SimpleCaptchaException('Field text must not be empty.')

        if not self.size:
            raise SimpleCaptchaException('Size must not be empty.')

        if not self.fontsize:
            raise SimpleCaptchaException('Font size must be defined.')

        if random_bgcolor:
            self.bgcolor = self._random_color()

    def _center_coords(self, draw, font):
        width, height = draw.textsize(self.text, font)
        xy = (self.size[0] - width) / 2., (self.size[1] - height) / 2.
        return xy

    def _add_noise_dots(self, draw):
        size = self.image.size
        for _ in range(int(size[0] * size[1] * 0.1)):
            draw.point((random.randint(0, size[0]),
                       random.randint(0, size[1])),
                       fill='white')
        return draw

    def _add_noise_lines(self, draw):
        size = self.image.size
        for _ in range(8):
            width = random.randint(1, 2)
            start = (0, random.randint(0, size[1] - 1))
            end = (size[0], random.randint(0, size[1] -1))
            draw.line([start, end], fill='white', width=width)
        for _ in range(8):
            start = (-50, -50)
            end = (size[0] + 10, random.randint(0, size[1] + 10))
            draw.arc(start + end, 0, 360, fill='white')
        return draw

    def _random_text(self):
        letters = string.ascii_lowercase + string.ascii_uppercase
        random_text = ""
        for _ in range(self.length):
            random_text += random.choice(letters)
        return random_text

    def _random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)

    def get_captcha(self, size=None, text=None, bgcolor=None):
        if text is not None:
            self.text = text
        if size is not None:
            self.size = size
        if bgcolor is not None:
            self.bgcolor = bgcolor

        self.image = Image.new('RGB', self.size, self.bgcolor)
        # font = ImageFont.truetype('./VERDANA.TTF', self.fontsize)
        font = ImageFont.truetype('/home/liubin/shop_backend/verify_utils/VERDANA.TTF', self.fontsize)
        # font = ImageFont.load_default().font
        draw = ImageDraw.Draw(self.image)
        xy = self._center_coords(draw, font)
        draw.text(xy=xy, text=self.text, font=font)

        draw = self._add_noise_dots(draw)
        draw = self._add_noise_lines(draw)
        # self.image.show()
        # self.image.save('./' + self.text + '.jpeg', 'JPEG', quality=95)
        return self.image, self.text


if __name__ == '__main__':
    sc = SimpleCaptcha(length=5, fontsize=36, random_text=True, random_bgcolor=True)
    img, text = sc.get_captcha()
    print(text)
    img.save('./' + text + '.jpeg', 'JPEG', quality=95)

