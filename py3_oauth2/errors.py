#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# File Name: ".expand("%"))
# Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
# Author LiuBin on: Fri Feb  9 17:00:24 CST 2018
#
# @desc:
#
# @history
#


class MissingCodeError(Exception):
    """
    用户点击同意后，获取access_token时code为空报错
    """
    error = 'missing_code'


class TokenExpiredError(Exception):
    error = 'token_expired'


class InsecureTransportError(Exception):
    error = 'insecure_transport'
    description = 'OAuth 2 MUST utilize https.'


class MismatchingStateError(Exception):
    error = 'mismatching_state'
    description = 'CSRF Warning! State not equal in request and response.'


class MissingTokenError(Exception):
    error = 'missing_token'


class MissingTokenTypeError(Exception):
    error = 'missing_token_type'


