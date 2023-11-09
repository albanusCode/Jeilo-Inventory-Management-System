import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import ProductForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductListView(View):
    def get(self, request):
        products = Product.objects.filter(is_deleted=False)
        return render(request, 'product.html', {'products': products})


class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    template_name = "product.html"
    success_url = '/products'
    success_message = "Product has been created successfully"
    form_class = ProductForm

    def form_valid(self, form):
        form.instance.is_deleted = False
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Product'
        context["savebtn"] = 'Add to products'
        return context

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        products = Product.objects.filter(is_deleted=False)
        context = {
            'form': form,
            'products': products,
        }
        return self.render_to_response(context)

    def form_valid(self, form):
        form.instance.is_deleted = False
        return super().form_valid(form)


def product_delete(request, pk):
    product = Product.objects.get(id = pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect("products")
    return render(request, 'product_delete.html')


def product_update(request, pk):
    product = Product.objects.get(id = pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("products")
    else:
        form = ProductForm(instance=product)
    context = {
        "form": form,
    }
    return render(request, 'product_update.html', context)



def export_products_to_csv(request):
    products = Product.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['code', 'Name', 'Type', 'Description', 'Quantity'])  # Write header row

    for product in products:
        writer.writerow([product.code, product.name, product.type, product.description, product.quantity])  # Write data rows

    return response
