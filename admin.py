# Register your models here.
from django.contrib import admin
from app.models import Question, Choice, Supplier, Merchandise, Store, Staff, Stock, Promotion, PromotionAffects
from app.models import Customer, Transaction, TransactionItem, Transfer, Shipment


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Supplier._meta.concrete_fields]
    search_fields = ['supplierName']

@admin.register(Merchandise)
class MerchandiseAdmin(admin.ModelAdmin):
    list_filter = ("supplierID",)
    list_display = [field.name for field in Merchandise._meta.concrete_fields]
    search_fields = ['name']


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Store._meta.concrete_fields]


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Staff._meta.concrete_fields]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Stock._meta.concrete_fields]


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Promotion._meta.concrete_fields]


@admin.register(PromotionAffects)
class PromotionAffectsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PromotionAffects._meta.concrete_fields]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.concrete_fields]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["transactionID", "customerID", "purchaseDate", "totalPrice", "storeID"]


@admin.register(TransactionItem)
class TransactionItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TransactionItem._meta.concrete_fields]
    list_filter = ["transactionID"]


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Transfer._meta.concrete_fields]
    list_filter = ["fromStoreID", "toStoreID"]


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Shipment._meta.concrete_fields]
    list_filter = ["storeID"]
