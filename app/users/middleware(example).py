from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        #logger.warning('1. before get_response')
        #return HttpResponse('1. before get response') #Before View!!!

        response = self.get_response(request)
        
        # Code to be executed for each request/response after
        # the view is called.
        #logger.warning('4. after get_response')
        #return HttpResponse('4. after response') #After View!!!

        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # process_view() is called just before Django calls the view.
        # It should return either None or an HttpResponse object
        # 若返回None，則繼續處理request並往下執行適當的view。
        # 若返回HttpResponse，則不用多花時間調用其他view，直接應用。
        #logger.warning('2. between req and res')
        #return HttpResponse('2. between req and res') #Before View!!! (ONLY for Module, Not global)

        return None

    def process_exception(self, request, exception):
        # Django calls process_exception() when a view raises an exception.
        # process_exception() should return either None or an HttpResponse object.
        #logger.warning('---- exception.args ----')

        return None

    def process_template_response(self, request, response):
        # return TemplateResponse object(render相關)
        #logger.warning('3. after view') #After View!!! (Required template render)

        return response