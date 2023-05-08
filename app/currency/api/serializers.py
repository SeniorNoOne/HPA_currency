from rest_framework import serializers

from currency.models import Rate, Source, ContactUs, RequestResponseLog
from utils.mixins import SendFeedbackMailMixin


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            'id',
            'buy',
            'sell',
            'created',
            'source',
        )


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = (
            'url',
            'code',
            'city',
            'phone',
        )


class ContactUsSerializer(serializers.ModelSerializer, SendFeedbackMailMixin):
    class Meta:
        model = ContactUs
        fields = (
            'email_from',
            'subject',
            'message',
        )

    def create(self, validated_data):
        mail = self._create_email(validated_data)
        self._send_mail(mail)
        return ContactUs(**validated_data)


class RequestResponseLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestResponseLog
        fields = (
            'path',
            'request_method',
            'time',
        )
