from django.conf import settings    
from django.utils.translation import activate     
import re

from django.utils.deprecation import MiddlewareMixin

class ForceInEnglish(MiddlewareMixin):
    def process_request(self, request):   
        if re.match(".*admin/", request.path):          
            activate("en")      
        else:
            activate(settings.LANGUAGE_CODE)
