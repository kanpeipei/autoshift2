from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class IndexViews(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'top/index.html')


index = IndexViews.as_view()

