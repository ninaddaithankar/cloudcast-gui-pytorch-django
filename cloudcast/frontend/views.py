import os

from django.shortcuts import render
from .forms import UploadFileForm

# Create your views here.
current_dir = os.path.dirname(os.path.realpath(__file__))


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if not os.path.isdir(os.path.join(current_dir, 'uploads')):
                os.mkdir(os.path.join(current_dir, 'uploads'))

            path = os.path.join(current_dir, 'uploads',
                                str(request.FILES['file']))

            with open(path, 'wb+') as destination:
                for chunk in request.FILES['file'].chunks():
                    destination.write(chunk)
            print('Successfully uploaded')

    else:
        form = UploadFileForm()
    return render(request, 'frontend/index.html', {'form': form})
