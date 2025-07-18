from django import forms
from .models import Product, OrderDetail , Comment

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        exclude = ['created_at', 'updated_at' , 'product']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

