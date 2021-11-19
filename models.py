from django.db import models
from django.db.models.deletion import CASCADE, RESTRICT, SET_NULL
from django.db.models.fields import AutoField, DateTimeField, DecimalField, EmailField, FloatField
from django.db.models.fields.related import ForeignKey
from django.utils.translation import activate
import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.question.question_text + ": " + self.choice_text


class Supplier(models.Model):
    supplierID = models.AutoField(primary_key=True)
    supplierName = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    emailAddress = models.EmailField(max_length=100)

    def __str__(self):
        return self.supplierName


class Merchandise(models.Model):
    merchandiseID = models.AutoField(primary_key=True)
    supplierID = models.ForeignKey(Supplier, on_delete=RESTRICT)
    name = models.CharField(max_length=512)
    regularPrice = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    buyPrice = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)
    productionDate = models.DateField()
    expirationDate = models.DateField()

    def __str__(self):
        return "{}: {}| {}".format(self.name, self.buyPrice, self.regularPrice)


class Store(models.Model):
    storeID = models.AutoField(primary_key=True)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    managerID = models.ForeignKey("Staff", on_delete=SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.address

    
class Staff(models.Model):
    staffID = models.AutoField(primary_key=True)
    storeID = models.ForeignKey(Store, on_delete=RESTRICT)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    salary = models.IntegerField(default=50000, blank=True)
    address = models.CharField(max_length=255)
    dateJoined = models.DateField(default=datetime.datetime.now)
    age = models.IntegerField(default=25)

    def __str__(self):
        return "{} {} at {}".format(self.firstName, self.lastName, self.storeID)


class Stock(models.Model):
    storeID = models.ForeignKey(Store, on_delete=RESTRICT)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=RESTRICT)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return "Store: {} | Merch {} | Quantity: {}".format(self.storeID, self.merchandiseID.merchandiseName, self.quantity)


class Promotion(models.Model):
    promotionID = models.AutoField(primary_key=True)
    discount = models.DecimalField(max_digits=32, decimal_places=0)
    startDate = models.DateField(default=datetime.datetime.now)
    validThrough = models.DateField()
    storeID = models.ForeignKey(Store, on_delete=RESTRICT)

    def __str__(self):
        return "ID: {} | discount: {} | validThrough: {}".format(self.promotionID, self.discount, self.validThrough)


class PromotionAffects(models.Model):
    promotionID = models.ForeignKey(Promotion, on_delete=CASCADE)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=CASCADE)

    def __str__(self):
        return "promotionID: {} | MerchandiseID: {}".format(self.promotionID, self.merchandiseID)


class Customer(models.Model):
    customerID = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    emailAddress = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    homeAddress = models.CharField(max_length=100)
    membershipLevel = models.CharField(choices=(("GOLD", "GOLD"), ("PLATINUM", "PLATINUM")), max_length=20)
    activeStatus = models.CharField(choices=(("ACTIVE", "ACTIVE"), ("INACTIVE", "INACTIVE")), max_length=20)
    validUntil = models.DateField()

    def __str__(self):
        return "{} {}".format(self.firstName, self.lastName)

class Transaction(models.Model):
    transactionID = models.AutoField(primary_key=True)
    customerID = models.ForeignKey(Customer, on_delete=SET_NULL, null=True)  # in case customer request deletion of data. 
    purchaseDate = models.DateTimeField(auto_now_add=True)
    totalPrice = models.DecimalField(max_digits=30, decimal_places=2)
    storeID = models.ForeignKey(Store, on_delete=RESTRICT)

    def __str__(self):
        return "transactionID: {} | purchaseDate: {} | total: {}".format(self.transactionID, self.purchaseDate, self.totalPrice)


class TransactionItem(models.Model):
    transactionItemID = models.AutoField(primary_key=True)
    transactionID = models.ForeignKey(Transaction, on_delete=CASCADE)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=SET_NULL, null=True)
    finalPrice = models.DecimalField(max_digits=30, decimal_places=2)
    totalPrice = models.DecimalField(max_digits=30, decimal_places=2)
    quantity = models.IntegerField(default=1)
    isReturn = models.BooleanField(default=False)

    def __str__(self):
        return "transactionID: {} | finalPrice: {}".format(self.transactionID, self.finalPrice)


class Transfer(models.Model):
    transferID = models.AutoField(primary_key=True)
    fromStoreID = models.ForeignKey(Store, on_delete=RESTRICT, related_name="transfer_out")
    toStoreID = models.ForeignKey(Store, on_delete=RESTRICT, related_name="transfer_in")
    managerID = models.ForeignKey(Staff, on_delete=RESTRICT)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=RESTRICT)
    quantity = models.IntegerField()
    dateOfTransfer = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "transferID: {} | quantity: {}".format(self.transferID, self.quantity)
    


class Shipment(models.Model):
    shipmentID = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=30, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    merchandiseID = models.ForeignKey(Merchandise, on_delete=RESTRICT)
    storeID = models.ForeignKey(Store, on_delete=RESTRICT)
    quantity = models.IntegerField()

    def __str__(self):
        return "shipmentID: {} | date: {}".format(self.shipmentID, self.date)


class SignUp(models.Model):
    storeID = models.ForeignKey(Store, on_delete=RESTRICT)
    staffID = models.ForeignKey(Staff, on_delete=RESTRICT)
    customerID = models.ForeignKey(Customer, on_delete=SET_NULL, null=True)  # GDPR
    date = models.DateField(auto_now_add=True)

