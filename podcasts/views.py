from django.shortcuts import render
from .models import Episode
from django.views import View
from django.http import HttpRequest,HttpResponse
from django.core.paginator import Paginator
# Create your views here.
class HomePage(View):
    template_name = 'index.html'
    def get(self,request):
        podcasts = Episode.objects.all()

        paginator = Paginator(podcasts,10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)


        context = {
            "title": 'Home page',
            "podcasts": page_obj
        }
        return render(request,self.template_name,context)
    
   