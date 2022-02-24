# -*- coding: utf-8 -*-
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from datetime import datetime
from .models import Attendance
import csv


def index(request):
    return render(request, 'scanner/qrcode.html')


def generator(request):
    return render(request, 'scanner/generator.html')


def logs(request):
    attendance_list = Attendance.objects.all()

    end_date = request.GET.get('end_date', None)
    start_date = request.GET.get('start_date', None)

    if end_date:
        datetime_object = datetime.strptime(end_date, '%B %d %Y')
        attendance_list = attendance_list.filter(time_stamp__lte=datetime_object)

    if start_date:
        datetime_object = datetime.strptime(start_date, '%B %d %Y')
        attendance_list = attendance_list.filter(time_stamp__gte=datetime_object)

    attendance_list = attendance_list.order_by('-time_stamp')

    page = request.GET.get('page', 1)

    paginator = Paginator(attendance_list, 100)

    try:
        attendance = paginator.page(page)
    except PageNotAnInteger:
        attendance = paginator.page(1)
    except EmptyPage:
        attendance = paginator.page(paginator.num_pages)

    return render(request, 'scanner/logs.html', {'Attendance': attendance})


def export(request):
    attendance_list = Attendance.objects.all()

    end_date = request.POST.get('end_date', None)
    start_date = request.POST.get('start_date', None)

    if end_date:
        datetime_object = datetime.strptime(end_date, '%B %d %Y')
        attendance_list = attendance_list.filter(time_stamp__lte=datetime_object)

    if start_date:
        datetime_object = datetime.strptime(start_date, '%B %d %Y')
        attendance_list = attendance_list.filter(time_stamp__gte=datetime_object)

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


def add(request):
    data = request.POST['data'].split('<data>')
    error_message = None
    student_name = None

    if len(data) == 5:
        student_id = data[0]
        last_name = data[1]
        first_name = data[2]
        middle_initial = data[3]

        try:
            attendance = Attendance(student_id=student_id,
                                    last_name=last_name,
                                    first_name=first_name,
                                    middle_initial=middle_initial,
                                    time_stamp=timezone.now()
                                    )
            attendance.save()
            student_name = last_name + ', ' + first_name + ' ' + middle_initial
        except Exception:
            error_message = "Failed to save attendance for student " + student_id
    else:
        error_message = "Wrong format."

    data = {
        "error_message": error_message or "",
        "student_name": student_name or "",
    }
    json_data = json.dumps(data)

    return HttpResponse(json_data, content_type='application/json')
