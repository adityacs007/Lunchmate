from django.shortcuts import render_to_response
from django.template.context import RequestContext
import logging
from httplib import HTTPResponse
from django.http import Http404


def home(request):
   context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
   return render_to_response('thirdauth/home.html',
                             context_instance=context)

def index(request):
   context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
   return render_to_response('thirdauth/index.html',
                             context_instance=context)
   
def adi(request):
   logging.info('views.adi')
   context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
   return render_to_response('thirdauth/home.html',
                             context_instance=context)
   
def adi_test(request):
   logging.info('views.adi_test')
   #raise Http404
   html = "<html><body>Hello!</body></html>"
   return HTTPResponse(html)