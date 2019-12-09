from django.shortcuts import render
from django.views.generic import View
from .models import Members
from .forms import MembersForm


# Create your views here.
class MembersListView(View):
    def get(self, request, *args, **kwargs):
        queryset = Members.objects.all().order_by('partner_number')
        return render(request, 'member/list.html', {'members': queryset})


members_list = MembersListView.as_view()


class MembersAddView(View):
    def get(self, request,  *args, **kwargs):
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



