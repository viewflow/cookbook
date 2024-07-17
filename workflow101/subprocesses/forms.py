from viewflow.forms import ModelForm, InlineFormSetField
from .models import OrderProcess, OrderItem


class OrderForm(ModelForm):
    order_items = InlineFormSetField(
        parent_model=OrderProcess,
        model=OrderItem,
        fields=['title', 'quantity'])

    class Meta:
        model = OrderProcess
        fields = ['customer_name', 'customer_address']
