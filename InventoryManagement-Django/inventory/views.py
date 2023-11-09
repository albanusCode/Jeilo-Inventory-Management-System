from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    View,
    CreateView, 
    UpdateView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Stock, Accessories
from .forms import StockForm, AccessoriesForm
from django_filters.views import FilterView
from .filters import StockFilter, AccessoriesFilter
from transactions.models import PurchaseBill
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse
import csv


class StockListView(LoginRequiredMixin, FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(is_deleted=False)
    template_name = 'material/inventory.html'
    paginate_by = 10


class StockCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
    model = Stock                                                                       # setting 'Stock' model as model
    form_class = StockForm                                                              # setting 'StockForm' form as form
    template_name = "material/edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = 'material/'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock has been created successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Material'
        context["savebtn"] = 'Add to Inventory'
        return context       


class StockUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):                                 # updateview class to edit stock, mixin used to display message
    model = Stock                                                                       # setting 'Stock' model as model
    form_class = StockForm                                                              # setting 'StockForm' form as form
    template_name = "material/edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = reverse_lazy('inventory')                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock has been updated successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Material'
        context["savebtn"] = 'Update Material'
        context["delbtn"] = 'Delete Material'
        return context


class StockDeleteView(LoginRequiredMixin, View):                                                            # view class to delete stock
    template_name = "material/delete_stock.html"                                                 # 'delete_stock.html' used as the template
    success_message = "Stock has been deleted successfully"                             # displays message when form is submitted
    
    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'object' : stock})

    def post(self, request, pk):  
        stock = get_object_or_404(Stock, pk=pk)
        stock.delete()                                               
        messages.success(request, self.success_message)
        return redirect('inventory')
    

def export_stocks_to_csv(request):
    stocks = Stock.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="materials.csv"'

    writer = csv.writer(response)
    writer.writerow(['Material', 'Code','Units', 'Quantity', 'Value', 'Received By', 'Date'])  # Write header row

    for stock in stocks:
        writer.writerow([stock.name, stock.code, stock.units, stock.quantity, stock.value, stock.receive, stock.time.date()])  # Write data rows

    return response





class AccessoriesListView(LoginRequiredMixin, FilterView):
    filterset_class = AccessoriesFilter
    queryset = Accessories.objects.filter(is_deleted=False)
    template_name = 'accessory/Accessories.html'
    paginate_by = 10


class AccessoriesCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
    model = Accessories                                                                       # setting 'Stock' model as model
    form_class = AccessoriesForm                                                              # setting 'StockForm' form as form
    template_name = "accessory/edit_accessories.html"                                                   # 'edit_stock.html' used as the template
    success_url = 'accessories/'                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Accessory has been created successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Add Accessory'
        context["savebtn"] = 'Add to Inventory'
        return context       


class AccessoriesUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):                                 # updateview class to edit stock, mixin used to display message
    model = Accessories                                                                       # setting 'Stock' model as model
    form_class = AccessoriesForm                                                              # setting 'StockForm' form as form
    template_name = "accessory/edit_accessories.html"                                                   # 'edit_stock.html' used as the template
    success_url = reverse_lazy('Accessories')                                                          # redirects to 'inventory' page in the url after submitting the form
    success_message = "Accessory has been updated successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Accessory'
        context["savebtn"] = 'Update Accessory'
        context["delbtn"] = 'Delete Accessory'
        return context


class AccessoriesDeleteView(LoginRequiredMixin, View):                                                            # view class to delete stock
    template_name = "accessory/delete_accessories.html"                                                 # 'delete_stock.html' used as the template
    success_message = "Accessory has been deleted successfully"                             # displays message when form is submitted
    
    def get(self, request, pk):
        accessory = get_object_or_404(Accessories, pk=pk)
        return render(request, self.template_name, {'object' : accessory})

    def post(self, request, pk):  
        accessory = get_object_or_404(Accessories, pk=pk)
        accessory.is_deleted = True
        accessory.save()                                               
        messages.success(request, self.success_message)
        return redirect('Accessories')


def export_accessories_to_csv(request):
    accessories = Accessories.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="accessories.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Size', 'Quantity', 'Value', 'Received By'])  # Write header row

    for accessory in accessories:
        writer.writerow([accessory.name, accessory.size, accessory.quantity, accessory.value, accessory.receive])  # Write data rows

    return response    