from django.shortcuts import render, redirect
from django.views.generic import View
from member.models import Members
from datetime import date
import locale
from .models import RequestedShifts
from .forms import RequestedShiftsForm, YearMonthForm

# Create your views here.


class ShiftsListViews(View):
    def get(self, request, *args, **kwargs):
        form = YearMonthForm
        if 'write_year' in request.session and 'write_month' in request.session:
            year = request.session['write_year']
            month = request.session['write_month']
            shifts = RequestedShifts.objects.all().filter(
                year=year,
                month=month
            ).order_by(
                'member__partner_number',
                'day'
            )
            return render(request, 'shift/list.html', {
                'shifts': shifts,
                'form': form,
                'year': year,
                'month': month,
                'days': range(1, 16),
                # 'day_of_week': day_of_week(int(year), int(month), 1),
                # 'weekday_dict': {'0': '月',
                #                  '1': '火',
                #                  '2': '水',
                #                  '3': '木',
                #                  '4': '金',
                #                  '5': '土',
                #                  '6': '日'
                #                  }
            })
        else:
            return render(request, 'shift/list.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = YearMonthForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            request.session['write_year'] = year
            request.session['write_month'] = month

            if not RequestedShifts.objects.all().filter(year=year, month=month).exists():
                for member in Members.objects.all():
                    for day in range(1, 16):
                        queryset = RequestedShifts(
                            member=member, year=year, month=month, day=day
                        )
                        queryset.save()
            shifts = RequestedShifts.objects.all().filter(
                year=year,
                month=month
            ).order_by('member__partner_number')
            return render(request, 'shift/list.html', {
                'shifts': shifts,
                'form': form,
                'year': year,
                'month': month,
                'days': range(1, 16),
            })
        else:
            return render(request, 'shift/list.html', {'form': form})


shifts_list = ShiftsListViews.as_view()


class ShiftsWriteViews(View):
    def get(self, request, partner_number, year, month, *args, **kwargs):
        shifts = RequestedShifts.objects.all().filter(
            member__partner_number=partner_number,
            year=year,
            month=month
        ).order_by('day')
        forms = []
        for shift in shifts:
            initial = {
                'since': shift.since,
                'to': shift.to,
                'is_absence': shift.is_absence
            }
            forms.append(RequestedShiftsForm(initial=initial, prefix=shift.day))
        return render(request, 'shift/write.html', {'forms': forms, 'partner_number': partner_number})

    def post(self, request, partner_number, year, month, *args, **kwargs):
        shifts = RequestedShifts.objects.all().filter(
            member__partner_number=partner_number,
            year=year,
            month=month
        ).order_by('day')
        for shift in shifts:
            form = RequestedShiftsForm(request.POST, prefix=shift.day)
            if form.is_valid():
                shift.since = form.cleaned_data['since']
                shift.to = form.cleaned_data['to']
                shift.is_absence = form.cleaned_data['is_absence']
                shift.save()
                # return render(request, 'shift/complete.html', {'form': shift.is_absence})
            else:
                error = "エラーが発生しました"
                return redirect('shift:write')
        return render(request, 'shift/complete.html')


shifts_write = ShiftsWriteViews.as_view()


# def day_of_week(year, month, day):
#     locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')
#     d = date(year, month, day)
#     return d.weekday()