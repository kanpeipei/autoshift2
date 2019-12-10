from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import YearMonthForm
from .models import FinalAllShifts, FinalSmgShifts, FinalCounterShifts, FinalKitchenShifts, FinalPersonalShifts
from shift.models import RequestedShifts
from member.models import Members
import random


class CreateShiftViews(View):
    def get(self, request, *args, **kwargs):
        form = YearMonthForm
        return render(request, 'create/create_1.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = YearMonthForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
        else:
            return render(request, 'create/create_1.html', {'form': form})
        auto_create(year, month)
        shifts = FinalAllShifts.objects.all().filter(year=year, month=month).order_by('day')
        return render(request, 'create/create_2.html', {
            'year': year,
            'month': month,
            'days': range(1, 16),
            'form': form,
            'shifts': shifts
        })


create = CreateShiftViews.as_view()


def auto_create(year, month):
    requested_shifts = RequestedShifts.objects.all().filter(year=year, month=month)
    candidate_shifts = [requested_shift for requested_shift in requested_shifts if not requested_shift.is_absence]
    choice_members = []
    for day in range(1, 16):
        final_day_shifts = dict.fromkeys([
            'opener',
            'closer'
            'counter_am1',
            'counter_am2',
            'counter_am3',
            'counter_am4',
            'counter_pm1',
            'counter_pm2',
            'counter_pm3',
            'kitchen_am1',
            'kitchen_pm1',
            'kitchen_pm2',
        ])
        day_shifts = [candidate_shift for candidate_shift in candidate_shifts
                      if candidate_shift.day == day
                      ]
        opener_shifts = [day_shift for day_shift in day_shifts
                         if day_shift.member.is_opener and day_shift.since == 9]
        smg_shifts = [day_shift for day_shift in day_shifts
                      if day_shift.member.is_smg and day_shift.to == 22]
        counter_am1_shifts = [day_shift for day_shift in day_shifts
                              if day_shift.member.is_counter and day_shift.since <= 9]
        counter_am2_shifts = [day_shift for day_shift in day_shifts
                              if day_shift.member.is_counter and day_shift.since <= 10]
        counter_am3_shifts = [day_shift for day_shift in day_shifts
                              if day_shift.member.is_counter and day_shift.since <= 11]
        counter_am4_shifts = [day_shift for day_shift in day_shifts
                              if day_shift.member.is_counter and day_shift.since <= 12]
        counter_pm1_shifts = [day_shift for day_shift in day_shifts
                              if day_shift.member.is_counter and day_shift.to == 22]
        # counter_pm2_shifts = [day_shift for day_shift in day_shifts
        #                       if day_shift.member.is_counter and day_shift.to == 22]
        # counter_pm3_shifts = [day_shift for day_shift in day_shifts
        #                       if day_shift.member.is_counter and day_shift.to == 22]
        kitchen_am1_shifts = [day_shift for day_shift in day_shifts
                              if day_shift.member.is_kitchen and day_shift.since == 9 and day_shift.to >= 17]
        kitchen_pm1_shifts = [day_shift for day_shift in day_shifts
                              if day_shift.member.is_kitchen and day_shift.since <= 17 and day_shift.to == 22]
        # kitchen_pm2_shifts = [day_shift for day_shift in day_shifts
        #                       if day_shift.member.is_kitchen and day_shift.to == 22]

        choice_members.clear()
        final_smg_shifts = FinalSmgShifts()
        if opener_shifts:
            final_day_shifts['opener'] = random.choice(opener_shifts)
            if final_day_shifts['opener'].to >= 17:
                final_personal_shifts_opener = FinalPersonalShifts(
                    member=final_day_shifts['opener'].member,
                    since=9,
                    to=17
                )
            else:
                final_personal_shifts_opener = FinalPersonalShifts(
                    member=final_day_shifts['opener'].member,
                    since=9,
                    to=final_day_shifts['opener'].to
                )
            final_personal_shifts_opener.save()
            final_smg_shifts.open_shifts = final_personal_shifts_opener

            if final_day_shifts['opener'] in counter_am1_shifts:
                counter_am1_shifts.remove(final_day_shifts['opener'])
            if final_day_shifts['opener'] in counter_am2_shifts:
                counter_am2_shifts.remove(final_day_shifts['opener'])
            if final_day_shifts['opener'] in counter_am3_shifts:
                counter_am3_shifts.remove(final_day_shifts['opener'])
            if final_day_shifts['opener'] in counter_am4_shifts:
                counter_am4_shifts.remove(final_day_shifts['opener'])
            if final_day_shifts['opener'] in counter_pm1_shifts:
                counter_pm1_shifts.remove(final_day_shifts['opener'])
            # if final_day_shifts['opener'] in counter_pm2_shifts:
            #     counter_pm2_shifts.remove(final_day_shifts['opener'])
            # if final_day_shifts['opener'] in counter_pm3_shifts:
            #     counter_pm3_shifts.remove(final_day_shifts['opener'])
            if final_day_shifts['opener'] in kitchen_am1_shifts:
                kitchen_am1_shifts.remove(final_day_shifts['opener'])
            if final_day_shifts['opener'] in kitchen_pm1_shifts:
                kitchen_pm1_shifts.remove(final_day_shifts['opener'])
            # if final_day_shifts['opener'] in kitchen_pm2_shifts:
            #     kitchen_pm2_shifts.remove(final_day_shifts['opener'])

            if final_day_shifts['opener'].to >= 17:
                choice_members = [smg_shift for smg_shift in smg_shifts
                                  if smg_shift.since <= 17
                                  ]
                # for smg_shift in smg_shifts:
                #     if smg_shift.since <= 17:
                #         choice_members.append(smg_shift)
            elif final_day_shifts['opener'].to < 17:
                choice_members = [smg_shift for smg_shift in smg_shifts
                                  if smg_shift.since <= final_day_shifts['opener'].to
                                  ]
                # for smg_shift in smg_shifts:
                #     if smg_shift.since <= final_day_shifts['opener'].to:
                #         choice_members.append(smg_shift)
        else:
            # クローズメンバーの候補を選択
            choice_members = [smg_shift for smg_shift in smg_shifts
                              if smg_shift.since <= 17
                              ]
            # for smg_shift in smg_shifts:
            #     if smg_shift.since <= 17:
            #         choice_members.append(smg_shift)
        if choice_members:
            final_day_shifts['closer'] = random.choice(choice_members)
            choice_members.clear()
            if final_day_shifts['closer']:
                if final_day_shifts['opener'].to < 17:
                    final_personal_shifts_closer = FinalPersonalShifts(
                        member=final_day_shifts['closer'].member,
                        since=final_day_shifts['opener'].to,
                        to=22
                    )
                else:
                    final_personal_shifts_closer = FinalPersonalShifts(
                        member=final_day_shifts['closer'].member,
                        since=17,
                        to=22
                    )
            else:
                final_personal_shifts_closer = FinalPersonalShifts(
                    member=final_day_shifts['closer'].member,
                    since=17,
                    to=22
                )

            final_personal_shifts_closer.save()
            final_smg_shifts.close_shifts = final_personal_shifts_closer

            if final_day_shifts['closer'] in counter_am1_shifts:
                counter_am1_shifts.remove(final_day_shifts['closer'])
            if final_day_shifts['closer'] in counter_am2_shifts:
                counter_am2_shifts.remove(final_day_shifts['closer'])
            if final_day_shifts['closer'] in counter_am3_shifts:
                counter_am3_shifts.remove(final_day_shifts['closer'])
            if final_day_shifts['closer'] in counter_am4_shifts:
                counter_am4_shifts.remove(final_day_shifts['closer'])
            if final_day_shifts['closer'] in counter_pm1_shifts:
                counter_pm1_shifts.remove(final_day_shifts['closer'])
            # if final_day_shifts['closer'] in counter_pm2_shifts:
            #     counter_pm2_shifts.remove(final_day_shifts['closer'])
            # if final_day_shifts['closer'] in counter_pm3_shifts:
            #     counter_pm3_shifts.remove(final_day_shifts['closer'])
            if final_day_shifts['closer'] in kitchen_am1_shifts:
                kitchen_am1_shifts.remove(final_day_shifts['closer'])
            if final_day_shifts['closer'] in kitchen_pm1_shifts:
                kitchen_pm1_shifts.remove(final_day_shifts['closer'])
            # if final_day_shifts['closer'] in kitchen_pm2_shifts:
            #     kitchen_pm2_shifts.remove(final_day_shifts['closer'])

        final_smg_shifts.save()

        final_counter_shifts = FinalCounterShifts()
        counter_am = []
        if counter_am1_shifts:
            # カウンター午前メンバーを決定
            final_day_shifts['counter_am1'] = random.choice(counter_am1_shifts)
            if final_day_shifts['counter_am1'].to < 17:
                counter_am.append(final_day_shifts['counter_am1'].to)
                final_personal_shifts_counter_am1 = FinalPersonalShifts(
                    member=final_day_shifts['counter_am1'].member,
                    since=9,
                    to=final_day_shifts['counter_am1'].to
                )
            else:
                final_personal_shifts_counter_am1 = FinalPersonalShifts(
                    member=final_day_shifts['counter_am1'].member,
                    since=9,
                    to=17
                )
            final_personal_shifts_counter_am1.save()
            final_counter_shifts.am1_shifts = final_personal_shifts_counter_am1
            # シフトが決定したパートナーを各ポジションから除外
            if final_day_shifts['counter_am1'] in counter_am2_shifts:
                counter_am2_shifts.remove(final_day_shifts['counter_am1'])
            if final_day_shifts['counter_am1'] in counter_am3_shifts:
                counter_am3_shifts.remove(final_day_shifts['counter_am1'])
            if final_day_shifts['counter_am1'] in counter_am4_shifts:
                counter_am4_shifts.remove(final_day_shifts['counter_am1'])
            if final_day_shifts['counter_am1'] in kitchen_am1_shifts:
                kitchen_am1_shifts.remove(final_day_shifts['counter_am1'])
            if final_day_shifts['counter_am1'] in kitchen_pm1_shifts:
                kitchen_pm1_shifts.remove(final_day_shifts['counter_am1'])
            # if final_day_shifts['counter_am1'] in kitchen_pm2_shifts:
            #     kitchen_pm2_shifts.remove(final_day_shifts['counter_am1'])
        if counter_am2_shifts:
            # カウンター午前メンバーを決定
            final_day_shifts['counter_am2'] = random.choice(counter_am2_shifts)
            if final_day_shifts['counter_am2'].to < 17:
                counter_am.append(final_day_shifts['counter_am2'].to)
                final_personal_shifts_counter_am2 = FinalPersonalShifts(
                    member=final_day_shifts['counter_am2'].member,
                    since=10,
                    to=final_day_shifts['counter_am2'].to
                )
            else:
                final_personal_shifts_counter_am2 = FinalPersonalShifts(
                    member=final_day_shifts['counter_am2'].member,
                    since=10,
                    to=17
                )
            final_personal_shifts_counter_am2.save()
            final_counter_shifts.am2_shifts = final_personal_shifts_counter_am2
            # シフトが決定したパートナーを各ポジションから除外
            if final_day_shifts['counter_am2'] in counter_am3_shifts:
                counter_am3_shifts.remove(final_day_shifts['counter_am2'])
            if final_day_shifts['counter_am2'] in counter_am4_shifts:
                counter_am4_shifts.remove(final_day_shifts['counter_am2'])
            if final_day_shifts['counter_am2'] in kitchen_am1_shifts:
                kitchen_am1_shifts.remove(final_day_shifts['counter_am2'])
            if final_day_shifts['counter_am2'] in kitchen_pm1_shifts:
                kitchen_pm1_shifts.remove(final_day_shifts['counter_am2'])
            # if final_day_shifts['counter_am2'] in kitchen_pm2_shifts:
            #     kitchen_pm2_shifts.remove(final_day_shifts['counter_am2'])
        if counter_am3_shifts:
            # カウンター午前メンバーを決定
            final_day_shifts['counter_am3'] = random.choice(counter_am3_shifts)
            if final_day_shifts['counter_am3'].to < 17:
                counter_am.append(final_day_shifts['counter_am3'].to)
                final_personal_shifts_counter_am3 = FinalPersonalShifts(
                    member=final_day_shifts['counter_am3'].member,
                    since=11,
                    to=final_day_shifts['counter_am3'].to
                )
            else:
                final_personal_shifts_counter_am3 = FinalPersonalShifts(
                    member=final_day_shifts['counter_am3'].member,
                    since=11,
                    to=17
                )
            final_personal_shifts_counter_am3.save()
            final_counter_shifts.am3_shifts = final_personal_shifts_counter_am3
            # シフトが決定したパートナーを各ポジションから除外
            if final_day_shifts['counter_am3'] in counter_am4_shifts:
                counter_am4_shifts.remove(final_day_shifts['counter_am3'])
            if final_day_shifts['counter_am3'] in kitchen_am1_shifts:
                kitchen_am1_shifts.remove(final_day_shifts['counter_am3'])
            if final_day_shifts['counter_am3'] in kitchen_pm1_shifts:
                kitchen_pm1_shifts.remove(final_day_shifts['counter_am3'])
            # if final_day_shifts['counter_am3'] in kitchen_pm2_shifts:
            #     kitchen_pm2_shifts.remove(final_day_shifts['counter_am3'])
        if counter_am4_shifts:
            # カウンター午前メンバーを決定
            final_day_shifts['counter_am4'] = random.choice(counter_am4_shifts)
            if final_day_shifts['counter_am4'].to < 17:
                counter_am.append(final_day_shifts['counter_am4'].to)
                final_personal_shifts_counter_am4 = FinalPersonalShifts(
                    member=final_day_shifts['counter_am4'].member,
                    since=12,
                    to=final_day_shifts['counter_am4'].to
                )
            else:
                final_personal_shifts_counter_am4 = FinalPersonalShifts(
                    member=final_day_shifts['counter_am4'].member,
                    since=12,
                    to=17
                )
            final_personal_shifts_counter_am4.save()
            final_counter_shifts.am4_shifts = final_personal_shifts_counter_am4
            # シフトが決定したパートナーを各ポジションから除外
            if final_day_shifts['counter_am4'] in kitchen_am1_shifts:
                kitchen_am1_shifts.remove(final_day_shifts['counter_am4'])
            if final_day_shifts['counter_am4'] in kitchen_pm1_shifts:
                kitchen_pm1_shifts.remove(final_day_shifts['counter_am4'])
            # if final_day_shifts['counter_am4'] in kitchen_pm2_shifts:
            #     kitchen_pm2_shifts.remove(final_day_shifts['counter_am4'])

        if counter_pm1_shifts:
            if counter_am:
                # list.sort(counter_am, reverse=True)
                loop = len(counter_am) - 2
                counter_am.sort()
                counter_am = counter_am[0:loop]
                # final_personal_shifts_pm1 = None
                # final_personal_shifts_pm2 = None
                # final_personal_shifts_pm3 = None
                final_day_shifts['counter_pm1'] = None
                final_day_shifts['counter_pm2'] = None
                final_day_shifts['counter_pm3'] = None
                for counter in counter_am:
                    choice_members = [counter_pm1_shift for counter_pm1_shift in counter_pm1_shifts
                                      if counter_pm1_shift.since <= counter.to
                                      ]
                    if final_day_shifts['counter_pm1'] is None and choice_members:
                        final_day_shifts['counter_pm1'] = random.choice(choice_members)
                        final_personal_shifts_counter_pm1 = FinalPersonalShifts(
                            member=final_day_shifts['counter_pm1'].member,
                            since=counter.to,
                            to=22
                        )
                        final_personal_shifts_counter_pm1.save()
                        final_counter_shifts.pm1_shifts = final_personal_shifts_counter_pm1
                        if final_day_shifts['counter_pm1'] in counter_pm1_shifts:
                            counter_pm1_shifts.remove(final_day_shifts['counter_pm1'])
                        if final_day_shifts['counter_pm1'] in kitchen_am1_shifts:
                            kitchen_am1_shifts.remove(final_day_shifts['counter_pm1'])
                        if final_day_shifts['counter_pm1'] in kitchen_pm1_shifts:
                            kitchen_pm1_shifts.remove(final_day_shifts['counter_pm1'])
                    elif final_day_shifts['counter_pm2'] is None and choice_members:
                        final_day_shifts['counter_pm2'] = random.choice(choice_members)
                        final_personal_shifts_counter_pm2 = FinalPersonalShifts(
                            member=final_day_shifts['counter_pm2'].member,
                            since=counter.to,
                            to=22
                        )
                        final_personal_shifts_counter_pm2.save()
                        final_counter_shifts.pm2_shifts = final_personal_shifts_counter_pm2
                        if final_day_shifts['counter_pm2'] in counter_pm1_shifts:
                            counter_pm1_shifts.remove(final_day_shifts['counter_pm2'])
                        if final_day_shifts['counter_pm2'] in kitchen_am1_shifts:
                            kitchen_am1_shifts.remove(final_day_shifts['counter_pm2'])
                        if final_day_shifts['counter_pm2'] in kitchen_pm1_shifts:
                            kitchen_pm1_shifts.remove(final_day_shifts['counter_pm2'])

                    elif final_day_shifts['counter_pm3'] is None and choice_members:
                        final_day_shifts['counter_pm3'] = random.choice(choice_members)
                        final_personal_shifts_counter_pm3 = FinalPersonalShifts(
                            member=final_day_shifts['counter_pm3'].member,
                            since=counter.to,
                            to=22
                        )
                        final_personal_shifts_counter_pm3.save()
                        final_counter_shifts.pm3_shifts = final_personal_shifts_counter_pm3
                        if final_day_shifts['counter_pm3'] in counter_pm1_shifts:
                            counter_pm1_shifts.remove(final_day_shifts['counter_pm3'])
                        if final_day_shifts['counter_pm3'] in kitchen_am1_shifts:
                            kitchen_am1_shifts.remove(final_day_shifts['counter_pm3'])
                        if final_day_shifts['counter_pm3'] in kitchen_pm1_shifts:
                            kitchen_pm1_shifts.remove(final_day_shifts['counter_pm3'])

                counter_am.clear()
                if final_day_shifts['counter_pm2'] is None and counter_pm1_shifts:
                    final_day_shifts['counter_pm2'] = random.choice(counter_pm1_shifts)
                    final_personal_shifts_counter_pm2 = FinalPersonalShifts(
                        member=final_day_shifts['counter_pm2'].member,
                        since=17,
                        to=22
                    )
                    final_personal_shifts_counter_pm2.save()
                    final_counter_shifts.pm2_shifts = final_personal_shifts_counter_pm2
                    if final_day_shifts['counter_pm2'] in counter_pm1_shifts:
                        counter_pm1_shifts.remove(final_day_shifts['counter_pm2'])
                    if final_day_shifts['counter_pm2'] in kitchen_am1_shifts:
                        kitchen_am1_shifts.remove(final_day_shifts['counter_pm2'])
                    if final_day_shifts['counter_pm2'] in kitchen_pm1_shifts:
                        kitchen_pm1_shifts.remove(final_day_shifts['counter_pm2'])

                if final_day_shifts['counter_pm3'] is None and counter_pm1_shifts:
                    final_day_shifts['counter_pm3'] = random.choice(counter_pm1_shifts)
                    final_personal_shifts_counter_pm3 = FinalPersonalShifts(
                        member=final_day_shifts['counter_pm3'].member,
                        since=17,
                        to=22
                    )
                    final_personal_shifts_counter_pm3.save()
                    final_counter_shifts.pm3_shifts = final_personal_shifts_counter_pm3
                    if final_day_shifts['counter_pm3'] in counter_pm1_shifts:
                        counter_pm1_shifts.remove(final_day_shifts['counter_pm3'])
                    if final_day_shifts['counter_pm3'] in kitchen_am1_shifts:
                        kitchen_am1_shifts.remove(final_day_shifts['counter_pm3'])
                    if final_day_shifts['counter_pm3'] in kitchen_pm1_shifts:
                        kitchen_pm1_shifts.remove(final_day_shifts['counter_pm3'])
            else:
                if counter_pm1_shifts:
                    final_day_shifts['counter_pm1'] = random.choice(counter_pm1_shifts)
                    final_personal_shifts_counter_pm1 = FinalPersonalShifts(
                        member=final_day_shifts['counter_pm1'].member,
                        since=17,
                        to=22
                    )
                    final_personal_shifts_counter_pm1.save()
                    final_counter_shifts.pm1_shifts = final_personal_shifts_counter_pm1
                    if final_day_shifts['counter_pm1'] in counter_pm1_shifts:
                        counter_pm1_shifts.remove(final_day_shifts['counter_pm1'])
                    if final_day_shifts['counter_pm1'] in kitchen_am1_shifts:
                        kitchen_am1_shifts.remove(final_day_shifts['counter_pm1'])
                    if final_day_shifts['counter_pm1'] in kitchen_pm1_shifts:
                        kitchen_pm1_shifts.remove(final_day_shifts['counter_pm1'])

                if counter_pm1_shifts:
                    final_day_shifts['counter_pm2'] = random.choice(counter_pm1_shifts)
                    final_personal_shifts_counter_pm2 = FinalPersonalShifts(
                        member=final_day_shifts['counter_pm2'].member,
                        since=17,
                        to=22
                    )
                    final_personal_shifts_counter_pm2.save()
                    final_counter_shifts.pm2_shifts = final_personal_shifts_counter_pm2
                    if final_day_shifts['counter_pm2'] in counter_pm1_shifts:
                        counter_pm1_shifts.remove(final_day_shifts['counter_pm2'])
                    if final_day_shifts['counter_pm2'] in kitchen_am1_shifts:
                        kitchen_am1_shifts.remove(final_day_shifts['counter_pm2'])
                    if final_day_shifts['counter_pm2'] in kitchen_pm1_shifts:
                        kitchen_pm1_shifts.remove(final_day_shifts['counter_pm2'])

                if counter_pm1_shifts:
                    final_day_shifts['counter_pm3'] = random.choice(counter_pm1_shifts)
                    final_personal_shifts_counter_pm3 = FinalPersonalShifts(
                        member=final_day_shifts['counter_pm3'].member,
                        since=17,
                        to=22
                    )
                    final_personal_shifts_counter_pm3.save()
                    final_counter_shifts.pm3_shifts = final_personal_shifts_counter_pm3
                    if final_day_shifts['counter_pm3'] in counter_pm1_shifts:
                        counter_pm1_shifts.remove(final_day_shifts['counter_pm3'])
                    if final_day_shifts['counter_pm3'] in kitchen_am1_shifts:
                        kitchen_am1_shifts.remove(final_day_shifts['counter_pm3'])
                    if final_day_shifts['counter_pm3'] in kitchen_pm1_shifts:
                        kitchen_pm1_shifts.remove(final_day_shifts['counter_pm3'])
        final_counter_shifts.save()

        final_kitchen_shifts = FinalKitchenShifts()
        if kitchen_am1_shifts and kitchen_am1_shifts:
            final_day_shifts['kitchen_am1'] = random.choice(kitchen_am1_shifts)
            final_personal_shifts_kitchen_am1 = FinalPersonalShifts(
                member=final_day_shifts['kitchen_am1'].member,
                since=9,
                to=17
            )
            final_personal_shifts_kitchen_am1.save()
            final_kitchen_shifts.am1_shifts = final_personal_shifts_kitchen_am1
        if kitchen_pm1_shifts and kitchen_pm1_shifts:
            final_day_shifts['kitchen_pm1'] = random.choice(kitchen_pm1_shifts)
            final_personal_shifts_kitchen_pm1 = FinalPersonalShifts(
                member=final_day_shifts['kitchen_pm1'].member,
                since=17,
                to=22
            )
            final_personal_shifts_kitchen_pm1.save()
            final_kitchen_shifts.pm1_shifts = final_personal_shifts_kitchen_pm1
            if final_day_shifts['kitchen_pm1'] in kitchen_pm1_shifts:
                kitchen_pm1_shifts.remove(final_day_shifts['kitchen_pm1'])
        if kitchen_pm1_shifts and kitchen_pm1_shifts:
            final_day_shifts['kitchen_pm2'] = random.choice(kitchen_pm1_shifts)
            final_personal_shifts_kitchen_pm2 = FinalPersonalShifts(
                member=final_day_shifts['kitchen_pm2'].member,
                since=17,
                to=22
            )
            final_personal_shifts_kitchen_pm2.save()
            final_kitchen_shifts.pm2_shifts = final_personal_shifts_kitchen_pm2

        final_kitchen_shifts.save()

        if FinalAllShifts.objects.filter(year=year, month=month, day=day).exists():
            final_all_shifts = FinalAllShifts.objects.all().get(
                year=year,
                month=month,
                day=day,
            )
            final_all_shifts.smg_shifts = final_smg_shifts
            final_all_shifts.counter_shifts = final_counter_shifts
            final_all_shifts.kitchen_shifts = final_kitchen_shifts
        else:
            final_all_shifts = FinalAllShifts(
                year=year,
                month=month,
                day=day,
                smg_shifts=final_smg_shifts,
                counter_shifts=final_counter_shifts,
                kitchen_shifts=final_kitchen_shifts
            )
        final_all_shifts.save()





