from urllib.parse import urlencode
from bs4 import BeautifulSoup

from django.template import Context, Template
from django.urls import reverse


def test_rate_urls_tag(client, rates_pagination):
    # Custom template tag (concat_urls) is implicitly called during
    # rendering templates with pagination. So pagination and custom
    # template tag are tested together as well as filtering by buy field
    buy, rates = rates_pagination

    filter_params = {'buy': buy}
    base_url = reverse('currency:rate-list')
    url = base_url + '?' + urlencode(filter_params)
    template_path = 'app/templates/rate/rate_list.html'

    # Accessing rate list link and getting context from it
    response = client.get(url)
    context = Context(response.context_data)

    # Opening template file and render it with appropriate context
    with open(template_path, 'r') as template_file:
        template_contents = template_file.read()
    template = Template(template_contents)
    rendered = template.render(context)

    # Looking up for pagination in HTML
    soup = BeautifulSoup(rendered, 'html.parser')
    pagination = soup.find('ul', {'class': 'pagination justify-content-center'})

    # Checking if ULRs in pagination are valid
    checks = [response.status_code == 200]
    for elem in pagination.find_all('a', {'class': 'page-link'}):
        url = base_url + elem['href']
        checks.append(client.get(url).status_code == 200)

    assert all(checks)
