from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Members
from .forms import MembersForm, MembersModifyForm


# Create your views here.
class MembersListView(View):
    def get(self, request, *args, **kwargs):
        queryset = Members.objects.all().order_by('partner_number')
        return render(request, 'member/list.html', {'members': queryset})


members_list = MembersListView.as_view()


class MembersAddView(View):
    def get(self, request, *args, **kwargs):
        form = MembersForm
        return render(request, 'member/add.html', {'form': form})

    def post(self, request,  *args, **kwargs):
        form = MembersForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.save()
        else:
            return render(request, 'member/add.html', {'form': form})

        return render(request, 'member/complete.html', {'member': form})


members_add = MembersAddView.as_view()


class MemberModifyView(View):
    def get(self, request, partner_number, *args, **kwargs):
        member = Members.objects.all().get(partner_number=partner_number)
        initial = {
            'name': member.name,
            'age': member.age,
            'hourly_pay': member.hourly_pay,
            'is_counter': member.is_counter,
            'is_fryer': member.is_fryer,
            'is_kitchen': member.is_kitchen,
            'is_smg': member.is_smg,
            'is_opener': member.is_opener,
        }
        form = MembersModifyForm(initial=initial)
        return render(request, 'member/modify.html', {'form': form})

    def post(self, request, partner_number, *args, **kwargs):
        form = MembersModifyForm(request.POST)
        member = Members.objects.all().get(partner_number=partner_number)
        if 'update' in request.POST:
            if form.is_valid():
                member.name = form.cleaned_data['name']
                member.age = form.cleaned_data['age']
                member.hourly_pay = form.cleaned_data['hourly_pay']
                member.is_counter = form.cleaned_data['is_counter']
                member.is_fryer = form.cleaned_data['is_fryer']
                member.is_kitchen = form.cleaned_data['is_kitchen']
                member.is_smg = form.cleaned_data['is_smg']
                member.is_opener = form.cleaned_data['is_opener']
                member.save()
            else:
                return render(request, 'member/modify.html', {'form': form, 'error': form.errors})
        elif 'delete' in request.POST:
            member.delete()
            return redirect('member:list')

        return render(request, 'member/complete.html', {'member': form})


members_modify = MemberModifyView.as_view()
