# -*- coding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from .models import Attendance, Section, Types
from django.db.models import Value as V
from django.db.models.functions import Concat
from .utils import is_teacher
import csv


@login_required
def index(request):
    return render(request, 'scanner/qrcode.html')


@login_required
@user_passes_test(is_teacher, login_url='/scanner', redirect_field_name=None)
def generator(request):
    types_list = Types.objects.all()
    section_list = Section.objects.all()
    return render(request, 'scanner/generator.html', {'Sections': section_list, 'Types': types_list})


@login_required
@user_passes_test(is_teacher, login_url='/scanner', redirect_field_name=None)
def logs(request):
    attendance_list = Attendance.objects.all()
    types_list = Types.objects.all()
    section_list = Section.objects.all()

    type = request.GET.get('type', None)
    name_field = request.GET.get('name_field', None)
    sections = request.GET.getlist('section', None)
    end_date = request.GET.get('end_date', None)
    start_date = request.GET.get('start_date', None)

    if end_date:
        datetime_object = datetime.strptime(end_date, '%B %d %Y')
        attendance_list = attendance_list.filter(time_stamp__lte=datetime_object)

    if start_date:
        datetime_object = datetime.strptime(start_date, '%B %d %Y')
        attendance_list = attendance_list.filter(time_stamp__gte=datetime_object)

    if sections:
        attendance_list = attendance_list.filter(section_id__in=sections)
        chosen_sections = section_list.filter(id__in=sections)

    if type:
        attendance_list = attendance_list.filter(user_type_id=type)

    if name_field:
        attendance_list = attendance_list.annotate(full_name=Concat('last_name', V(' '), 'first_name',
                                                                    V(' '), 'middle_initial'))\
            .filter(full_name__icontains=name_field)

    attendance_list = attendance_list.order_by('-time_stamp')

    page = request.GET.get('page', 1)

    paginator = Paginator(attendance_list, 100)

    try:
        attendance = paginator.page(page)
    except PageNotAnInteger:
        attendance = paginator.page(1)
    except EmptyPage:
        attendance = paginator.page(paginator.num_pages)

    return render(request, 'scanner/logs.html', {'Attendance': attendance,
                                                 'Sections': section_list,
                                                 'Types': types_list,
                                                 'chosen_sections': sections})


@login_required
@user_passes_test(is_teacher, login_url='/scanner', redirect_field_name=None)
def export(request):
    attendance_list = Attendance.objects.all()

    type = request.POST.get('type', None)
    name_field = request.POST.get('name_field', None)
    sections = request.POST.getlist('section', None)
    end_date = request.POST.get('end_date', None)
    start_date = request.POST.get('start_date', None)

    if end_date:
        datetime_object = datetime.strptime(end_date, '%B %d %Y')
        attendance_list = attendance_list.filter(time_stamp__lte=datetime_object)

    if start_date:
        datetime_object = datetime.strptime(start_date, '%B %d %Y')
        attendance_list = attendance_list.filter(time_stamp__gte=datetime_object)

    if sections:
        attendance_list = attendance_list.filter(section_id__in=sections)

    if type:
        attendance_list = attendance_list.filter(user_type_id=type)

    if name_field:
        attendance_list = attendance_list.annotate(full_name=Concat('last_name', V(' '), 'first_name',
                                                                    V(' '), 'middle_initial'))\
            .filter(full_name__icontains=name_field)

    opts = Attendance._meta
    response = HttpResponse()

    # force download.
    response['Content-Disposition'] = 'attachment;filename=export.csv'

    # the csv writer
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]

    # Write a first row with header information
    writer.writerow(field_names[1:])

    # Write data rows
    for obj in attendance_list:
        writer.writerow([getattr(obj, field) for field in field_names[1:]])

    return HttpResponse(response, content_type='text/csv')


@login_required
@user_passes_test(is_teacher, login_url='/scanner', redirect_field_name=None)
def add(request):
    data = request.POST['data'].split('<data>')
    error_message = None
    student_name = None

    if len(data) == 6:
        user_type = data[0]
        last_name = data[1]
        first_name = data[2]
        middle_initial = data[3]
        section = data[4]

        if user_type and last_name and first_name and middle_initial:
            student_name = last_name + ', ' + first_name + ' ' + middle_initial
            try:
                attendance = Attendance(user_type_id=user_type,
                                        last_name=last_name,
                                        first_name=first_name,
                                        middle_initial=middle_initial,
                                        time_stamp=timezone.now(),
                                        section_id=section
                                        )
                attendance.save()
            except Exception:
                error_message = "Failed to save attendance for student " + student_name
        else:
            error_message = "Failed to scan QR Code."
    else:
        error_message = "Wrong format."

    data = {
        "error_message": error_message or "",
        "student_name": student_name or "",
    }
    json_data = json.dumps(data)

    return HttpResponse(json_data, content_type='application/json')
