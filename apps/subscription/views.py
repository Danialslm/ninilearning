from django.views.generic import ListView

from .models import Plan


class PlanListView(ListView):
    model = Plan
    template_name = 'subscription/plan_list.html'
