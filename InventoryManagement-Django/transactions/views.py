import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import forms
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal

from django.urls import reverse, reverse_lazy
from .models import PurchaseBill, PurchaseItem
from .forms import PurchaseItemFormset
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View, 
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
    PurchaseBill, 
    Supplier, 
    PurchaseItem,
    PurchaseBillDetails,
    SaleBill,  
    SaleItem,
    SaleBillDetails, 
)
from .forms import (
    SelectSupplierForm, 
    PurchaseItemFormset,
    PurchaseDetailsForm, 
    SupplierForm, 
    SaleForm,
    SaleItemFormset,
    SaleDetailsForm,
    MaterialForm,
)
from inventory.models import Stock
from products.models import Product

from .models import Material

from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle




# shows a lists of all suppliers
class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = "suppliers/suppliers_list.html"
    queryset = Supplier.objects.filter(is_deleted=False)
    paginate_by = 10


# used to add a new supplier
class SupplierCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transactions/suppliers'
    success_message = "Supplier has been created successfully"
    template_name = "suppliers/edit_supplier.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Supplier'
        context["savebtn"] = 'Add Supplier'
        return context     


# used to update a supplier's info
class SupplierUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    success_url = '/transactions/suppliers'
    success_message = "Supplier details has been updated successfully"
    template_name = "suppliers/edit_supplier.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Supplier'
        context["savebtn"] = 'Save Changes'
        context["delbtn"] = 'Delete Supplier'
        return context


# used to delete a supplier
class SupplierDeleteView(LoginRequiredMixin, View):
    template_name = "suppliers/delete_supplier.html"
    success_message = "Supplier has been deleted successfully"

    def get(self, request, pk):
        supplier = get_object_or_404(Supplier, pk=pk)
        return render(request, self.template_name, {'object' : supplier})

    def post(self, request, pk):  
        supplier = get_object_or_404(Supplier, pk=pk)
        supplier.is_deleted = True
        supplier.save()                                               
        messages.success(request, self.success_message)
        return redirect('suppliers-list')


# used to view a supplier's profile
class SupplierView(LoginRequiredMixin, View):
    def get(self, request, name):
        supplierobj = get_object_or_404(Supplier, name=name)
        bill_list = PurchaseBill.objects.filter(supplier=supplierobj)
        page = request.GET.get('page', 1)
        paginator = Paginator(bill_list, 10)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)
        context = {
            'supplier': supplierobj,
            'bills': bills
        }
        return render(request, 'suppliers/supplier.html', context)





# shows the list of bills of all purchases 
class PurchaseView(LoginRequiredMixin, ListView):
    model = PurchaseBill
    template_name = "purchases/purchases_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


# used to select the supplier
class SelectSupplierView(LoginRequiredMixin, View):
    form_class = SelectSupplierForm
    template_name = 'purchases/select_supplier.html'

    def get(self, request, *args, **kwargs):                                    # loads the form page
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):                                   # gets selected supplier and redirects to 'PurchaseCreateView' class
        form = self.form_class(request.POST)
        if form.is_valid():
            supplierid = request.POST.get("supplier")
            supplier = get_object_or_404(Supplier, id=supplierid)
            return redirect('new-purchase', supplier.pk)
        return render(request, self.template_name, {'form': form})

# used to generate a bill object and save items
class PurchaseCreateView(LoginRequiredMixin, View):                                                 
    template_name = 'purchases/new_purchase.html'
    success_url = 'purchases/'                                                          # redirects to 'inventory' page in the url after submitting the form


    def get(self, request, pk):
        formset = PurchaseItemFormset(request.GET or None)                      # renders an empty formset
        supplierobj = get_object_or_404(Supplier, pk=pk)                        # gets the supplier object
        context = {
            'formset'   : formset,
            'supplier'  : supplierobj,
        }                                                                       # sends the supplier and formset as context
        return render(request, self.template_name, context)

    def post(self, request, pk):
        formset = PurchaseItemFormset(request.POST)  # receives a post method for the formset
        supplierobj = get_object_or_404(Supplier, pk=pk)  # gets the supplier object
        if formset.is_valid():
            billobj = PurchaseBill(supplier=supplierobj)
            billobj.save()

            billdetailsobj = PurchaseBillDetails(billno=billobj)
            billdetailsobj.save()

            for form in formset:
                billitem = form.save(commit=False)
                billitem.billno = billobj

                # Access the 'material' field data from the form
                material_name = form.cleaned_data['material']

                billitem.totalprice = billitem.perprice * billitem.quantity
                billitem.save()

            messages.success(request, "Purchased items have been registered successfully")
            return redirect('purchase-bill', billno=billobj.billno)
        formset = PurchaseItemFormset(request.GET or None)
        context = {
            'formset'   : formset,
            'supplier'  : supplierobj
        }
        return render(request, self.template_name, context)


# used to delete a bill object
class PurchaseDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = PurchaseBill
    template_name = "purchases/delete_purchase.html"
    success_url = '/transactions/purchases'
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = PurchaseItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity -= item.quantity
                stock.save()
        messages.success(self.request, "Purchase bill has been deleted successfully")
        return super(PurchaseDeleteView, self).delete(*args, **kwargs)




# shows the list of bills of all sales 
class SaleView(LoginRequiredMixin, ListView):
    model = SaleBill
    template_name = "sales/sales_list.html"
    context_object_name = 'bills'
    ordering = ['-time']
    paginate_by = 10


# used to generate a bill object and save items
class SaleCreateView(LoginRequiredMixin, View):                                                      
    template_name = 'sales/new_sale.html'

    def get(self, request):
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)                          # renders an empty formset
        stocks = Stock.objects.filter(is_deleted=False)
        context = {
            'form'      : form,
            'formset'   : formset,
            'stocks'    : stocks
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = SaleForm(request.POST)
        formset = SaleItemFormset(request.POST)                                 # recieves a post method for the formset
        if form.is_valid() and formset.is_valid():
            # saves bill
            billobj = form.save(commit=False)
            billobj.save()     
            # create bill details object
            billdetailsobj = SaleBillDetails(billno=billobj)
            billdetailsobj.save()
            
                        
            for form in formset:                                                # for loop to save each individual form as its own object
                # false saves the item and links bill to the item
                billitem = form.save(commit=False)
                billitem.billno = billobj                                       # links the bill object to the items
                # gets the stock item
                stock = get_object_or_404(Stock, name=billitem.stock.name)      
                # calculates the total price
                billitem.totalprice = billitem.perprice * billitem.pqty
                
                # updates quantity in stock db
                stock.quantity -= billitem.quantity   
                # saves bill item and stock
                stock.save()
                billitem.save()

            messages.success(request, "The order has been registered successfully")
            return redirect('sale-bill', billno=billobj.billno)
        form = SaleForm(request.GET or None)
        formset = SaleItemFormset(request.GET or None)
        context = {
            'form'      : form,
            'formset'   : formset,
        }
        return render(request, self.template_name, context)


# used to delete a bill object
class SaleDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = SaleBill
    template_name = "sales/delete_sale.html"
    success_url = '/transactions/sales'
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        items = SaleItem.objects.filter(billno=self.object.billno)
        for item in items:
            stock = get_object_or_404(Stock, name=item.stock.name)
            if stock.is_deleted == False:
                stock.quantity += item.quantity
                stock.save()
        messages.success(self.request, "Sale bill has been deleted successfully")
        return super(SaleDeleteView, self).delete(*args, **kwargs)




from django.templatetags.static import static  # Import static to get the path to the logo image
from reportlab.lib import colors
from reportlab.platypus.flowables import Image
from reportlab.lib.enums import TA_CENTER  # Import TA_CENTER from reportlab.lib.enums
from datetime import date



# used to display the purchase bill object
class PurchaseBillView(LoginRequiredMixin, View):
    model = PurchaseBill
    template_name = "bill/purchase_bill.html"
    bill_base = "bill/bill_base.html"

    

    def add_background(self, canvas, doc):
        # Draw a rectangle as the background on each page
        canvas.setFillColorRGB(0.75, 0.75, 0.75)
        canvas.rect(0, 0, landscape(letter)[0], landscape(letter)[1], fill=True, stroke=False)

    def get(self, request, billno):
        purchase_bill = PurchaseBill.objects.get(billno=billno)

        # Check if the request is for PDF download
        if 'download_pdf' in request.GET:

            # Create a response object with content type as 'application/pdf'
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Requisition.pdf"'

            # Create a PDF document
            doc = SimpleDocTemplate(response, pagesize=landscape(letter))
            elements = []

            # Register the onPage method to add the background on each page
            doc.build(
                self.get_elements(purchase_bill),
                onFirstPage=self.add_background,
                onLaterPages=self.add_background
            )

            return response
        
        # If it's not a PDF download request, proceed with rendering the template
        context = {
            'bill': purchase_bill,
            'items': PurchaseItem.objects.filter(billno=billno),
            'billdetails': PurchaseBillDetails.objects.get(billno=billno),
            'bill_base': self.bill_base,
        }
        return render(request, self.template_name, context)


            

    def get_elements(self, purchase_bill):
        # Add content to the PDF
        styles = getSampleStyleSheet()

        elements = []

        elements.append(Paragraph(f'REQUISITION FORM', styles['Heading1']))
        elements.append(Spacer(1, 6))

        company_name = "JEILO COLLECTIONS LTD"  # Replace with your actual company name
        title_style = ParagraphStyle(

            'TitleStyle',
            parent=styles['Heading1'],
            fontName='Times-Bold',
            fontSize=16,
            alignment=TA_CENTER,  # Set the alignment to the center
        )

        elements.append(Paragraph(company_name, title_style))
        elements.append(Spacer(1, 6))  # Add some space after the title

        # Center the additional information at the top using a Table


        bold_style = ParagraphStyle(
            'BoldStyle',
            parent=styles['Normal'],
            fontName='Times-Bold',
            fontSize=12
        )

        info_table = Table([
            [Paragraph('<b>DEALERS IN:</b> Handcrafted leather & textile bags', styles['Normal'])],
            [Paragraph('<b>REGD ADDRESS:</b> Ngong Road Professional Centre, 2nd Ngong Rd, Nairobi', styles['Normal'])],
            [Paragraph('<b>EMAIL:</b> info@jeilocollections.com', styles['Normal'])],
            [Spacer(1, 12)],  # Spacer to create some space between the information and other content
        ])

        # Set the alignment of the info_table to the left
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))

        # Create a new table to hold both info_table and the date
        info_and_date_table = Table([
            [info_table, Paragraph(f'<b>DATE:</b> {date.today().strftime("%Y-%m-%d")} ', styles['Normal'])],
        ])

        # Set the column widths to place info_table on the left and the date on the right
        info_and_date_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align the info_table to the left
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),   # Align the content to the top of the cell
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Add some right padding to the info_table cell
            ('LEFTPADDING', (-1, -1), (-1, -1), 10),  # Add some left padding to the date cell
            ('GRID', (0, 0), (-1, -1), 0.5, 'black'),  # Add borders to the table (optional)
        ]))

        # Add the info_and_date_table to the elements list
        elements.append(info_and_date_table)
        elements.append(Spacer(1, 12))


         # Add table for RECIPIENT and PHONE
        recipient_phone_info = [
            [
                Paragraph(f'<b>RECIPIENT:</b> {purchase_bill.supplier.name.upper()}', styles['Normal']),
                Paragraph(f'<b>PHONE:</b> {purchase_bill.supplier.phone}', styles['Normal']),
            ]
        ]

        # Adjust the colWidths based on your desired layout
        recipient_phone_table = Table(recipient_phone_info, colWidths=[300, 300])

        # Add the table to the elements list
        elements.append(recipient_phone_table)
        elements.append(Spacer(1, 24))

            

            # Add table for Purchase Items
        data = [['SL', 'Material', 'Quantity', 'Unit Price (KES)', 'Total Price']]
        for idx, item in enumerate(purchase_bill.get_items_list(), 1):
            data.append([idx, item.material, item.quantity, item.perprice, item.totalprice])

        padding = 6  # You can adjust this value as per your requirement

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), 'grey'),
            ('TEXTCOLOR', (0, 0), (-1, 0), 'black'),  # Black text color for the header row
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),  # Set the font to Courier New (Courier-Bold)
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'LightGrey'),

            # Add border margins to each cell
            ('TOPPADDING', (0, 0), (-1, -1), padding),
            ('BOTTOMPADDING', (0, 0), (-1, -1), padding),
            ('LEFTPADDING', (0, 0), (-1, -1), padding),
            ('RIGHTPADDING', (0, 0), (-1, -1), padding),

            # Add borders to the table
            ('GRID', (0, 0), (-1, -1), 1, 'black'),  # 1 is the border width
        ]))

        elements.append(table)  # Add the table to the PDF
        elements.append(Spacer(1, 24))

        # Add table for SUBTOTAL and TOTAL
        subtotal_total_info = [
            [
                Paragraph(f'<b>SUBTOTAL:</b> {purchase_bill.get_total_price()}', styles['Normal']),
                Paragraph(f'TOTAL(VAT Inc.):  {purchase_bill.get_grand_total()}',  bold_style)
            ]
        ]

        # Adjust the colWidths based on your desired layout
        subtotal_total_table = Table(subtotal_total_info, colWidths=[300, 300])

        # Add the table to the elements list
        elements.append(subtotal_total_table)
        elements.append(Spacer(1, 24))


        return elements


# used to display the sale bill object
import io
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


class SaleBillView(LoginRequiredMixin, View):
    model = SaleBill
    template_name = "bill/sale_bill.html"
    bill_base = "bill/bill_base.html" 
    # Your existing code...

    def generate_pdf_bill(self, context):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Quotation.pdf"'

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

         # Extract recipient name
        recipient_name = context["bill"].name

        # Table for reference number and order date
        reference_data = [['Reference Number', 'Order Date'],
                        [context["bill"].billno, context["bill"].time.date()]]

        # Table for additional information (7 columns)
        additional_data = [['SALESPERSON', 'SHIPPING METHOD', 'SHIPPING TERMS', 'DELIVERY DATE', 'PAYMENT TERMS', 'MODE OF PAYMENT', 'DUE DATE'],
                        ['Grace Mbugua', context["bill"].shipm, 'Invoice Payment/LPO', context["bill"].deliveryDate, context["bill"].paymentTerms, context["bill"].mode, context["bill"].dueDate ]]

        # Table for items
        data = [['#', 'Item', 'Description', 'Quantity', 'Price', 'Total']]
        items = context['items']
        subtotal = 0  # Variable to keep track of the subtotal

        for idx, item in enumerate(items, start=1):
            data.append([idx, item.product, item.description, item.quantity, item.perprice, item.totalprice])
            subtotal += item.totalprice  # Update the subtotal with each item's total price

        # Calculate the grand total (VAT inclusive)
        grand_total_vat_inc = subtotal * 1.16
        rounded_grand_total = round(grand_total_vat_inc, 2)  # Round off to 2 decimal place

        subtotal_total_info = [
            [
                Paragraph(f'<b>SUBTOTAL: {subtotal}</b>'),

            ],

            [
                Paragraph(f'<b>Total (VAT Inc.): {rounded_grand_total}</b>'),
            ]
        ]

        # Adjust the colWidths based on your desired layout
        subtotal_total_table = Table(subtotal_total_info, colWidths=610)


         # Create a custom Paragraph style for the title
        title_style = ParagraphStyle(
            name='TitleStyle',
            fontName='Times-Bold',
            fontSize=14,
            textColor=colors.black,
            alignment=TA_CENTER,  # Align the text to the center
            spaceAfter=4  # Add some space after the title
        )

            # Define the title text
        title_text = 'QUOTATION FORM'

        # Create a Paragraph element for the title
        title_paragraph = Paragraph(title_text, title_style)


        


         # Create a custom Paragraph style for the recipient's name
        recipient_style = ParagraphStyle(
            name='RecipientStyle',
            fontName='Times-Bold',
            fontSize=12,
            textColor=colors.black,
            alignment=TA_LEFT,  # Align the text to the left
            leftIndent=20  # Adjust the left indent here (in points)
        )


         # Creating empty table for the recipient's name
        recipient_table = Table([[Paragraph(f'<b>Recipient:</b> {recipient_name}', recipient_style)]], colWidths=755)

            # Table for company's address
        company_address = """
            <font size="12" face="Helvetica-Bold">DEALERS IN :</font> <font size="12">Handcrafted leather & textile bags</font><br/>
            <font face="Helvetica-Bold">REGD ADDRESS :</font> Ngong Road Professional Centre,<br/>
            2nd Ngong Rd, Nairobi<br/>
            <font face="Helvetica-Bold">EMAIL :</font> info@jeilocollections.com
        """
        company_address_style = ParagraphStyle(
            name='CompanyAddressStyle',
            fontName='Times',
            fontSize=10,
            textColor=colors.black,
            alignment=TA_CENTER  # Align the text to the center
        )

        # Creating table for company's address
        company_address_table = Table([[Paragraph(company_address, company_address_style)]], colWidths=[700])

        # Creating tables
        additional_table = Table(additional_data, colWidths=100, rowHeights=25)  # Adjust colWidths and rowHeights as needed
        reference_table = Table(reference_data, colWidths=350, rowHeights=25)
        items_table = Table(data, colWidths=100, rowHeights=25)

        # Applying styles to the tables
        reference_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Very dark text color
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        additional_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Very dark text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Very dark text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))



        # Adding tables to elements list
        elements = [ 
            title_paragraph,
            Spacer(1, 5),

            # Centered company address table
            Table([[company_address_table]], colWidths=[755], rowHeights=[100], style=[
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center the table
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center the content vertically
                ('LEFTPADDING', (0, 0), (-1, -1), 0),  # Remove left padding
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),  # Remove right padding
            ]),
            Spacer(1, 8),

            recipient_table,  # Display recipient's name in a separate table
            Spacer(1, 8),

            additional_table,
            Spacer(1, 8), 

            reference_table, 
            Spacer(1, 8), 
            
            items_table,
            Spacer(1, 8), 


            subtotal_total_table,  # Add the subtotal and total table to the elements list

            ]
        
        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    def get(self, request, billno):
        context = {
            'bill'          : SaleBill.objects.get(billno=billno),
            'items'         : SaleItem.objects.filter(billno=billno),
            'billdetails'   : SaleBillDetails.objects.get(billno=billno),
            'bill_base'     : self.bill_base,
        }

        # Check if the request wants a PDF download
        download_as_pdf = request.GET.get('download_pdf')
        if download_as_pdf:
            return self.generate_pdf_bill(context)

        return render(request, self.template_name, context)
    

class SupplierProfileView(LoginRequiredMixin, View):
    template_name = 'suppliers/supplier.html'

    def get(self, request, name):
        supplier = get_object_or_404(Supplier, name=name)
        materials = Material.objects.filter(supplier=supplier)
        bills = PurchaseBill.objects.filter(supplier=supplier)

        context = {
            'supplier': supplier,
            'materials': materials,
            'bills': bills
        }
        return render(request, self.template_name, context)

    def post(self, request, name):
        form = MaterialForm(request.POST)
        if form.is_valid():
            supplier = get_object_or_404(Supplier, name=name)
            material = form.save(commit=False)
            material.supplier = supplier
            material.save()
            return redirect('supplier', name=name)

        context = {'form': form}
        return render(request, self.template_name, context)
    
    
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage
from .models import Supplier

def send_inquiry_view(request, pk):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        supplier = get_object_or_404(Supplier, pk=pk)

        # Check if the file exists in the request.FILES before accessing it
        if 'file' in request.FILES:
            file = request.FILES['file']
        else:
            file = None

        # Create an EmailMessage object and attach the file if it exists
        email = EmailMessage(
            'Quotation Inquiry',
            message,
            'psychometric254@gmail.com',  # Replace with the sender's email address
            [supplier.email],  # Use the recipient's email from the supplier object
        )

        if file:
            email.attach(file.name, file.read(), file.content_type)

        email.send(fail_silently=False)

        # Perform any additional logic if needed

        messages.success(request, "Requisition email sent successfully.")
        return redirect('supplier', name=supplier.name)

class SupplierMaterialUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    form_class = MaterialForm
    success_url = '/transactions/suppliers/'
    success_message = "Supplier stock has been updated successfully"
    template_name = "suppliers/update_supplier_materials.html"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] =   "Update Supplier Stock"
        context["savebtn"] = 'Update'
        context["delbtn"] = 'Remove'
        return context


class SupplierMaterialDeleteView(LoginRequiredMixin, View):
    template_name = "suppliers/remove_supplier_materials.html"
    success_message = "Supplier stock has been deleted successfully"

    def get(self, request, material_id):
        material = get_object_or_404(Material, id=material_id)
        return render(request, self.template_name, {'object': material})

    def post(self, request, material_id):
        material = get_object_or_404(Material, id=material_id)
        material.delete()
        messages.success(request, "Supplier material has been deleted successfully")
        redirect_url = reverse('supplier', kwargs={'name': material.supplier.name})
        return redirect(redirect_url)
    


def export_orders_to_csv(request):
    orders = SaleItem.objects.select_related('billno').all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['Customer Name', 'Phone', 'Material', 'Product', 'Quantity'])  # Write header row

    for order in orders:
        customer_name = order.billno.name if order.billno else ''  # Get the customer name or empty string if billno is not set
        phone = order.billno.phone if order.billno else ''  # Get the customer phone or empty string if billno is not set
        writer.writerow([customer_name, phone, order.stock, order.product, order.pqty])  # Write data rows

    return response

def send_quotation_email(request):
    if request.method == 'POST':
        # Get the sale ID from the form data
        sale_id = request.POST.get('sale_id')

        # Get the message and file from the form data
        message = request.POST.get('message', '')
        uploaded_file = request.FILES.get('file' , None)

        # Retrieve the SaleBill object using the sale ID
        sale = get_object_or_404(SaleBill, pk=sale_id)

        # Get the customer's email address from the sale object
        customer_email = sale.email

        # Create the EmailMessage instance
        subject = 'JEILO COLLECTIONS: QUOTATION'
        body = f'{message}'
        email = EmailMessage(subject, body, to=[customer_email])

        # Attach the file to the email if it was uploaded
        if uploaded_file:
            file_name = uploaded_file.name
            file_content = uploaded_file.read()
            file_content_type = uploaded_file.content_type
            email.attach(file_name, file_content, file_content_type)

        # Send the email
        email.send()

        # Add a success message
        messages.success(request, 'Quotation email sent successfully!')

        # Redirect to the sales list page
        return redirect('send_quotation_email')

    # If the request method is not POST, render the sales list page
    # Pass the sales list to the template to display in the table
    sales = SaleBill.objects.all()  # Modify this query based on your requirements
    return render(request, 'sales/sales_list.html', {'bills': sales})