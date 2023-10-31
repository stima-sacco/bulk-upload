import os
from django.shortcuts import render, redirect

from app.models import Car
from .forms import CarForm
import pandas as pd
from django.core.files import File

def index(request):
    context = {}
    return render(request, 'app/index.html', context)


def bulk_upload_items(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            if excel_file.name.endswith('.xls') or excel_file.name.endswith('.xlsx'):
                df = pd.read_excel(excel_file)
                for index, row in df.iterrows():
                    item = Car(make=row['make'], brand=row['brand'])

                    filename = os.fsdecode(str(row['car_image']))
                    print('car_image : ' + str(row['car_image']))
                    print('filename : ' + str(filename))
                    file = open(filename, 'rb')
                    item.car_image.save('image.png', File(file))  # Make sure the column name matches the one in your Excel file
                    file.close()
                    item.save()
                    
                return redirect('app:bulk-upload')  # Redirect to a view that lists the uploaded items
        else:
            print('errors : ' + str(form.errors))
    else:
        form = CarForm()
    return render(request, 'app/upload.html', {'form': form})