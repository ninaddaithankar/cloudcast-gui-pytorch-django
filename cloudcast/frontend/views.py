import os
import numpy as np
import torch
from django.shortcuts import render
from .forms import UploadFileForm
from .cloudcast_autoencoder import runModel, save_images_cartopy

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Create your views here.
current_dir = os.path.dirname(os.path.realpath(__file__))


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if not os.path.isdir(os.path.join(current_dir, 'uploads')):
                os.mkdir(os.path.join(current_dir, 'uploads'))

            path = os.path.join(current_dir, 'uploads',
                                'sample.npy')

            with open(path, 'wb+') as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
            print('Successfully uploaded')
            img_X = np.load(os.path.join(current_dir, 'uploads/sample.npy'))
            save_images_cartopy(prediction_video=torch.tensor(img_X),
                                lines=False, high_res_map=False, name='output', path='./static/uploaded')
            runModel(img_X)

    else:
        form = UploadFileForm()
    return render(request, 'frontend/index.html', {'form': form})
