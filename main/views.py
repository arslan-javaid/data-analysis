from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
# from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
# from main.utils import URLUtil
from main.models import ScrapyItem

# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')


from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get(self, request):
        return render(request, self.template_name, {})


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)  # check if url format is valid
    except ValidationError:
        return False

    return True


@csrf_exempt
@require_http_methods(['POST', 'GET'])  # only get and post
def crawl(request):
    # Post requests are for new crawling tasks
    if request.method == 'POST':

        search_query = request.POST.get('search-query', None)
        as_ylo = request.POST.get('as_ylo', None)
        as_yhi = request.POST.get('as_yhi', None)

        if not search_query:
            return JsonResponse({'error': 'Missing  args'})

        search_query = search_query.replace(" ", "+")
        url = 'https://scholar.google.com.pk/scholar?hl=en&as_sdt=0%2C5&q='+search_query

        if as_ylo:
            url += 'as_ylo=' + as_ylo

        if as_yhi:
            url += 'as_ylo=' + as_yhi

        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is invalid'})

        domain = urlparse(url).netloc  # parse the url and extract the domain
        unique_id = str(uuid4())  # create a unique ID.

        # Custom settings for scrapy spider.
        settings = {
            'unique_id': unique_id,  # unique ID for each record for DB
            'search_query': search_query,
            'as_ylo': as_ylo,
            'as_yhi': as_yhi,
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        # Schedule a new crawling task from scrapyd.
        task = scrapyd.schedule('default', 'main',
                                settings=settings, url=url, domain=domain)

        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started'})

    # Get requests are for getting result of a specific crawling task
    elif request.method == 'GET':
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)

        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})

        # Possible results are -> pending, running, finished
        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                # this is the unique_id that we created even before crawling started.
                item = ScrapyItem.objects.get(unique_id=unique_id)
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})