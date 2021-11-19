from django.http import HttpResponse
from django.db import transaction
from app.models import Shipment, Store
from django.shortcuts import render
from django.forms import modelform_factory
from django.db import transaction
from django import forms

@transaction.atomic
def example1(request):
    # Example for operating with a model (table entry)
    obj = Shipment.objects.first()
    Form = modelform_factory(Shipment, exclude=[])
    if request.method == "GET":
        form = Form(instance=obj)
        return render(request, 'app/quickform.html', {'form': form})
    else:  # Post statement. 
        form = Form(request.POST, request.FILES)
        if form.is_valid():
            # maybe modify the stock here as well.
            form.save()
        return HttpResponse("OKAY")


# hand made form. 
@transaction.atomic
def example2(request):
    if request.method == "GET":
        greeting_phrase = "<h1> Hello, please fill this form. You're very smart. </h1>"
        current_name = "Jessica"
        color = "Green"
        return render(request, 'app/form1.html', {'greeting_phrase': greeting_phrase, 'color': color, 'current_name': current_name})
    else:  # Post statement. 
        name = request.POST["your_name"]
        color = request.POST["your_color"]
        return HttpResponse("Your name is {}. Your favorite color is {}. ".format(name, color))


class MyModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s | %s" % (obj.storeID, obj.address)

# programatic form with drop down options that are database entries. 
class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    your_color = forms.CharField(label='Your color', max_length=100)
    stores = MyModelMultipleChoiceField(label="Your store", queryset=Store.objects, )  # User can choose multiple just for demo


@transaction.atomic
def example3(request):
    # Example for operating with a model (table entry)
    obj = Shipment.objects.first()
    if request.method == "GET":
        form = NameForm(initial={"your_name": "John Curtain", "your_color": "blue"})
        return render(request, 'app/quickform.html', {'form': form})
    else:  # Post statement. 
        form = NameForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data["your_name"]
            color = form.cleaned_data["your_color"]
            stores = form.cleaned_data["stores"]  # this returns the list of stores that were selected, just for the demo
            store = stores.first()  # we dont' actually acre about other stores, just the first one. 
            return HttpResponse("Your name is {}. Your favorite color is {}. You work at {}. ".format(name, color, store.address))
        else:
            return HttpResponse("Bad request data. {}".format(form.errors), status=400)



def example4(request):
    # how to show a list of data with Jinja2 (django's template language)
    stores = Store.objects.all()
    funny_things_to_say = ["boo", "pew-woo", "yahoo"]
    return render(request, 'app/stores.html', {'stores': stores, "funny_things_to_say": funny_things_to_say})