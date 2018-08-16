from django.contrib import admin
from .models import Request, Volunteer, Contributor, DistrictNeed, DistrictCollection, DistrictManager
import csv
from django.http import HttpResponse

class RequestAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    readonly_fields = ('dateadded',)
    ordering = ('district',)
    def download_csv(self, request, queryset):
        f = open('test.csv', 'w')
        writer = csv.writer(f)
        l = []
        for i in (Request._meta.get_fields()):
            l.append(i.name)
        writer.writerow(l)
        data = Request.objects.all().values_list()
        for s in data:
            writer.writerow(s)
        f.close()
        f = open('test.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Requests.csv'
        return response

    list_filter = ('district', 'status',)


class VolunteerAdmin(admin.ModelAdmin):
    actions = ['download_csv']
    readonly_fields = ('joined',)
    list_display = ('name', 'phone', 'organisation', 'joined')
    list_filter = ('district', 'joined',)
    def download_csv(self, request, queryset):
        f = open('test.csv', 'w')
        writer = csv.writer(f)
        l = []
        for i in (Volunteer._meta.get_fields()):
            l.append(i.name)
        writer.writerow(l)
        data = Volunteer.objects.all().values_list()
        for s in data:
            writer.writerow(s)
        f.close()
        f = open('test.csv', 'r')
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Volunteers.csv'
        return response


class ContributorAdmin(admin.ModelAdmin):
    list_filter = ('district', 'status',)

admin.site.register(Request, RequestAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(DistrictNeed)
admin.site.register(DistrictCollection)
admin.site.register(DistrictManager)
