class OrderingMixin:
    def setup(self, *args, **kwargs):
        super(OrderingMixin, self).setup(*args, **kwargs)
        self.ordering = self.request.GET.get('ordering', 'id')

    def get_queryset(self):
        qs = super().get_queryset()
        if self.ordering:
            return qs.order_by(self.ordering)
        return qs
