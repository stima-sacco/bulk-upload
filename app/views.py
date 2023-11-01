import os
from django.shortcuts import render, redirect

from app.models import Car, CarBrand, ExtraCarImage
from .forms import CarForm
import pandas as pd
from django.core.files import File

def index(request):
    context = {}
    return render(request, 'app/index.html', context)

def carHasMainPhoto(car_directory_path):
    has_main_photo = False
    main_photo_path = ''
    main_image = ''
    file_name = ''

    for file in os.listdir(car_directory_path):
        file_path = ''.join([car_directory_path, '/', file])

        if os.path.isfile(file_path):
            parts = file.split('.')

            if len(parts) > 1:
                name = parts[0]
                file_name = file
                main_photo_path = ''.join([car_directory_path, '/', file])

                if name == "1":
                    has_main_photo = True
                    main_image = file
                    main_photo_path = ''.join([car_directory_path, '/', file])
                    break

    extra_images = []
    if has_main_photo:
        for file in os.listdir(car_directory_path):
            while True:
                if file == main_image:
                    break

                extra_image_path = ''.join([car_directory_path, '/', file])
                extra_images.append(extra_image_path)

                break

    return {
        'has_main_photo': has_main_photo,
        'file_name': file_name,
        'extra_images': extra_images,
        'main_photo_path': main_photo_path
    }

def bulk_upload_items(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        # if form.is_valid():
        excel_file = request.FILES['excel_file']
        upload_directory = r'C:/msacar_uploads'

        cars_directory = ''.join([upload_directory, '/', 'cars'])
        cars_directory_exists = os.path.exists(cars_directory)

        car_directories = []
        if cars_directory_exists:
            for car_directory in os.listdir(cars_directory):
                car_directories.append(car_directory)

                # car_folder_path = ''.join([cars_directory, '/', car_directory])
                # for car in os.listdir(car_folder_path):
                #     print(car)
                # print("=================")
                # if excel_file.name.endswith('.xls') or excel_file.name.endswith('.xlsx'):
            df = pd.read_excel(excel_file, 'CARS')
            for index, row in df.iterrows():
                car_folder_path = car_folder_path = ''.join([cars_directory, '/', row['directory']])
                response = carHasMainPhoto(car_folder_path)

                if response['has_main_photo']:
                # for car_img in os.listdir(car_folder_path):
                    car = Car()
                    car.vendor = "Vendor"
                    car.make = row['make']
                    car.body_type =  row['body_type']

                    car_brand = CarBrand.objects.get(pk=row['brand_id'])

                    car.brand = car_brand
                    file = open(response['main_photo_path'], 'rb')
                    car.car_image.save(response['file_name'], File(file))
                    file.close()

                    car.save()

                    for extra_image in response['extra_images']:
                        extra_car_image = ExtraCarImage()
                        extra_car_image.car = car
                        
                        file = open(extra_image, 'rb')
                        extra_car_image.car_image.save(os.path.basename(extra_image), File(file))
                        extra_car_image

                    print(car)
                print("============")
            # item = Car(make=row['make'], brand=row['brand'])

                #         filename = os.fsdecode(str(row['car_image']))
                #         print('car_image : ' + str(row['car_image']))
                #         print('filename : ' + str(filename))
                #         file = open(filename, 'rb')
                #         item.car_image.save('image.png', File(file))  # Make sure the column name matches the one in your Excel file
                #         file.close()
                #         item.save()
                        
            return redirect('app:bulk-upload')  # Redirect to a view that lists the uploaded items
            # else:
            #     print('errors : ' + str(form.errors))
    else:
        form = CarForm()
    return render(request, 'app/upload.html', {'form': form})