
from django import urls
from django.shortcuts import render, redirect
from converter import forms
from django.contrib.auth import login,logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
import requests
import json


# Create your views here.

def index(request):
    api_request = requests.get("http://api.exchangeratesapi.io/v1/latest?access_key=9ada4f69c415476e65a06b1346e8c90c&format=1")
    currency_dict = json.loads(api_request.text)

    currency_rates_dict = currency_dict['rates']
    list_of_country_currency_code = [x for x in currency_rates_dict.keys()]
    tuple_of_country_codes = [tuple([x,x]) for x in list_of_country_currency_code]

    currency_form = forms.CurrencyForm(tuple_of_country_codes,request.POST or None)

    converted_currency = ""
    if request.method == "POST":
        if currency_form.is_valid():

            # values from the html input fields
            source_currency_code = currency_form.cleaned_data['source_currency_code']
            target_currency_code = currency_form.cleaned_data['target_currency_code']
            input_currency_value = currency_form.cleaned_data['source_currency_value']

            # get live amount of selected country 
            from_country_base_value = currency_rates_dict[source_currency_code]
            to_country_base_value = currency_rates_dict[target_currency_code]
            
            # logic to calculate the converted_currency
            converted_currency = (to_country_base_value / from_country_base_value) * float(input_currency_value)
            context = {
                'currency_form':currency_form,
                'converted_currency':converted_currency
            }
            return render(request, 'converter/index.html', context)

    # form initialization
    context = {
        'currency_form': currency_form,
        'converted_currency':converted_currency
    }
    return render(request, 'converter/index.html', context)

def login_view(request):
    if request.method == "POST":
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # user = authenticate(username = username, password = password)
        # if user is not None:
        #     login(request,user)
        #     if request.user:
        #         messages.success(request, "Successfully Loged In...")
        #         return redirect("/index")
        #     else:
        #         messages.warning(request, "Please Login or sign up for new accout!!")
        #         return redirect('login/')
        # if user is not None:
        #     messages.warning(request, "Invalid User")
        #     return redirect('/login')
        # messages.warning(request, "Invalid User")
        # return redirect('/login')

        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            #login the user
            user = form.get_user()
            login(request,user)
            messages.success(request, "Successfully Loged In...")
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'converter/login.html', {'form':form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account is created...")
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'converter/signup.html', {'form':form})