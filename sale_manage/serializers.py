from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class OrderSerializer(serializers.Serializer):
    sum_amount = serializers.CharField(label=_("Sum amount"))
    sum_price = serializers.CharField(label=_("Sum price"),
                                      style={'input_type': 'Integer'})

    def validate(self, attrs):
        sum_amount = attrs.get('sum_amount')
        sum_price = attrs.get('sum_price')

        if sum_amount and sum_price:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs
