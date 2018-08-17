from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from .models import Request, Volunteer, DistrictManager, Contributor, DistrictNeed, RescueCampDetails
import django_filters
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.http import HttpResponseRedirect

class CreateRequest(CreateView):
    model = Request
    template_name='mainapp/request_form.html'
    fields = [
        'district',
        'location',
        'requestee',
        'requestee_phone',
        'is_request_for_others',
        'latlng',
        'latlng_accuracy',
        'needrescue',
        'detailrescue',
        'needwater',
        'detailwater',
        'needfood',
        'detailfood',
        'needcloth',
        'detailcloth',
        'needmed',
        'detailmed',
        'needkit_util',
        'detailkit_util',
        'needtoilet',
        'detailtoilet',
        'needothers'
    ]
    success_url = '/req_sucess'


class RegisterVolunteer(CreateView):
    model = Volunteer
    fields = ['name', 'district', 'phone', 'organisation', 'area', 'address']
    success_url = '/reg_success'


class RegisterContributor(CreateView):
    model = Contributor
    fields = ['name', 'district', 'phone', 'address',  'commodities']
    success_url = '/contrib_success'


class HomePageView(TemplateView):
    template_name = "home.html"


class ReqSuccess(TemplateView):
    template_name = "mainapp/req_success.html"


class RegSuccess(TemplateView):
    template_name = "mainapp/reg_success.html"


class ContribSuccess(TemplateView):
    template_name = "mainapp/contrib_success.html"

class DisclaimerPage(TemplateView):
    template_name = "mainapp/disclaimer.html"

class AboutIEEE(TemplateView):
    template_name = "mainapp/aboutieee.html"

class DistNeeds(TemplateView):
    template_name = "mainapp/district_needs.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['district_data'] = DistrictNeed.objects.all()
        return context


class RescueCamps(TemplateView):
    template_name = "mainapp/rescue_camps.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['camp_data'] = RescueCampDetails.objects.all()
        return context


class RequestFilter(django_filters.FilterSet):
    class Meta:
        model = Request
        # fields = ['district', 'status', 'needwater', 'needfood', 'needcloth', 'needmed', 'needkit_util', 'needtoilet', 'needothers',]

        fields = {
                    'district' : ['exact'],
                    'requestee' : ['icontains'],
                    'requestee_phone' : ['exact'],
                    'location' : ['icontains']
                 }

    def __init__(self, *args, **kwargs):
        super(RequestFilter, self).__init__(*args, **kwargs)
        # at startup user doen't push Submit button, and QueryDict (in data) is empty
        if self.data == {}:
            self.queryset = self.queryset.none()


def request_list(request):
    filter = RequestFilter(request.GET, queryset=Request.objects.all() )
    req_data = filter.qs.order_by('-dateadded')
    paginator = Paginator(req_data, 100)
    page = request.GET.get('page')
    req_data = paginator.get_page(page)
    return render(request, 'mainapp/request_list.html', {'filter': filter , "data" : req_data })


class DistrictManagerFilter(django_filters.FilterSet):
    class Meta:
        model = DistrictManager
        fields = ['district']

    def __init__(self, *args, **kwargs):
        super(DistrictManagerFilter, self).__init__(*args, **kwargs)
        # at startup user doen't push Submit button, and QueryDict (in data) is empty
        if self.data == {}:
            self.queryset = self.queryset.none()

def districtmanager_list(request):
    filter = DistrictManagerFilter(request.GET, queryset=DistrictManager.objects.all())
    return render(request, 'mainapp/districtmanager_list.html', {'filter': filter})

class Maintenance(TemplateView):
    template_name = "mainapp/maintenance.html"


def mapdata(request):
    data = Request.objects.exclude(latlng__exact="").values()

    return JsonResponse(list(data) , safe=False) 

def mapview(request):
    return render(request,"map.html")

def dmodash(request):
    return render(request , "dmodash.html")

def dmoinfo(request):
    if("district" not in request.GET.keys()):return HttpResponseRedirect("/")
    dist = request.GET.get("district")
    reqserve = Request.objects.all().filter(status = "sup" , district = dist).count()
    reqtotal = Request.objects.all().filter(district = dist).count()
    volcount = Volunteer.objects.all().filter(district = dist).count()
    conserve = Contributor.objects.all().filter(status = "ful" , district = dist).count()
    contotal = Contributor.objects.all().filter(district = dist).count()
    return render(request ,"dmoinfo.html",{"reqserve" : reqserve , "reqtotal" : reqtotal , "volcount" : volcount , "conserve" : conserve , "contotal" : contotal })
