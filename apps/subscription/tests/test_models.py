from django.test import TestCase
from django.urls import reverse, resolve

from apps.subscription.models import Plan, DiscountCode
from apps.subscription.views import PlanListView


class PlanModelsTestCase(TestCase):
    def test_plan_model_creation(self):
        plan = Plan.objects.create(
            plan_time=1,
            price=100000,
            discounted_price=90000,
        )

        self.assertEqual(plan.plan_time, 1)
        self.assertEqual(plan.price, 100000)
        self.assertEqual(plan.discounted_price, 90000)

    def test_discount_code_model_creation(self):
        discount_code = DiscountCode.objects.create()

        self.assertIsNotNone(discount_code.code)


class PlanViewsTestCase(TestCase):
    def setUp(self):
        self.url = reverse('subscription:plans')

    def test_correct_view_class(self):
        view = resolve(self.url)
        self.assertIs(
            view.func.view_class,
            PlanListView,
        )

    def test_view_load(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'subscription/plan_list.html')
