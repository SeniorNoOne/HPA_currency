from django import template

register = template.Library()


@register.filter
def concat_urls(first_url, second_url):
    return str(first_url) + '&' + str(second_url)
