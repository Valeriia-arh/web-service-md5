from md5 import count
import requests
from django.test import TestCase

from rest_framework.test import APIRequestFactory
#APIRequestFactory - creating test requests

test_file = "http://data.enteromics.com/robots.txt"

assertContains(response, text, ...)  # проверяет, что в ответе сервера содержится указанный текст;
assertTemplateUsed(response, template_name, ...)  # проверяет, что при рендеринге страницы использовался указанный шаблон;
assertRedirects(response, expected_url, ...)  # проверяет, было ли перенаправление;


def download_and_md5sum:
    
