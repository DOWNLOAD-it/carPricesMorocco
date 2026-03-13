from django.shortcuts import render


# Create your views here.
def predictForm(request):
    return render(request, "predict_form.html")
