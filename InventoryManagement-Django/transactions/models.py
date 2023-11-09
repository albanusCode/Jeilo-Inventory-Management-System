import datetime
from django import forms
from django.db import models
from inventory.models import Stock

#contains suppliers
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    kra = models.CharField(max_length=150, default="")
    phone = models.CharField(max_length=12, unique=True)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254, unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name


#contains the purchase bills made
class PurchaseBill(models.Model):
    billno = models.CharField(primary_key=True, max_length=4, editable=False)
    time = models.DateTimeField(auto_now=True)
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE, related_name='purchasesupplier')

    def save(self, *args, **kwargs):
        if not self.billno:
            last_bill = PurchaseBill.objects.order_by('-billno').first()
            if last_bill:
                last_bill_number = int(last_bill.billno)
                self.billno = str(last_bill_number + 1).zfill(4)
            else:
                self.billno = "0001"
        super().save(*args, **kwargs)

    def __str__(self):
	    return "Bill no: " + str(self.billno)
    
    def get_items_list(self):
        return PurchaseItem.objects.filter(billno=self)

    def get_total_price(self):
        purchaseitems = PurchaseItem.objects.filter(billno=self)
        total = 0
        
        for item in purchaseitems:
            total += item.totalprice
        return total
    
    def get_grand_total(self):
        purchaseitems = PurchaseItem.objects.filter(billno=self)
        global total 
        grand_total = 0
        for purchaseitem in purchaseitems:
            grand_total += purchaseitem.totalprice

        vat_grand_total = grand_total * 1.16
        return round(vat_grand_total)
        
    
#contains the purchase stocks made
class PurchaseItem(models.Model):
    billno = models.ForeignKey(PurchaseBill, on_delete = models.CASCADE, related_name='purchasebillno')
    material = models.CharField(max_length=150, default='')
    quantity = models.DecimalField(decimal_places=2, max_digits=8, default='')
    perprice = models.DecimalField(decimal_places=2, max_digits=8, default='')
    totalprice = models.FloatField(default=1)
   
    def __str__(self):
	    return "Bill no: " + str(self.billno.billno)

#contains the other details in the purchases bill
class PurchaseBillDetails(models.Model):
    billno = models.OneToOneField(PurchaseBill, on_delete = models.CASCADE, related_name='saledetailsbillno', primary_key=True)
    total = models.CharField(max_length=50, blank=True, null=True)
    
    
    def __str__(self):
	    return "Bill no: " + str(self.billno.billno)


#contains the sale bills made
class SaleBill(models.Model):
    billno = models.CharField(primary_key=True, max_length=4, editable=False)
    time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150)
    shipm = models.CharField(max_length=150, default='')
    deliveryDate = models.CharField(max_length=150, default='')
    paymentTerms = models.CharField(max_length=150, default='')
    mode = models.CharField(max_length=150, default=" ")
    dueDate = models.DateField(max_length=150, default=datetime.date.today)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    product= models.CharField(max_length=150, default=1)

    def save(self, *args, **kwargs):
        if not self.billno:
            last_bill = SaleBill.objects.order_by('-billno').first()
            if last_bill:
                last_bill_number = int(last_bill.billno)
                self.billno = str(last_bill_number + 1).zfill(4)
            else:
                self.billno = "0001"
        super().save(*args, **kwargs)

    def __str__(self):
	    return "Bill no: " + str(self.billno)

    def get_items_list(self):
        return SaleItem.objects.filter(billno=self)
    
    
    def get_total_price(self):  
            saleitems = SaleItem.objects.filter(billno=self)
            total = 0
            
            for item in saleitems:
                total += item.totalprice
            return total
    
    def get_total_price(self):
        saleitems = SaleItem.objects.filter(billno=self)
        total = 0
        
        for item in saleitems:
            total += item.totalprice
        return total
        
 
    
#contains the sale stocks made
class SaleItem(models.Model):
    billno = models.ForeignKey(SaleBill, on_delete = models.CASCADE, related_name='salebillno')
    stock = models.ForeignKey(Stock, on_delete = models.CASCADE, related_name='saleitem')
    product = models.CharField(max_length=150, default='')
    quantity = models.IntegerField(default=1)
    pqty = models.IntegerField(default=1)
    description = models.TextField(default='')
    perprice = models.IntegerField(default=1)
    totalprice = models.IntegerField(default=1)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno) + ", Item = " + self.stock.name

#contains the other details in the sales bill
class SaleBillDetails(models.Model):
    billno = models.OneToOneField(SaleBill, on_delete = models.CASCADE, related_name='saledetailsbillno', primary_key=True)

    total = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
	    return "Bill no: " + str(self.billno.billno)
    

class Material(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
 
