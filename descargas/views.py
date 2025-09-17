import os
from django.shortcuts import render, redirect
import yt_dlp
from django.contrib import messages
from django.http import HttpResponse


def video(request):
    return render(request, 'paginas/descargas.html')

def download_video(request):
    if request.method == 'POST':
            video_url = request.POST.get('url')
            if not video_url:
                messages.error(request, 'Please enter a valid URL.')
                return redirect('download_page')

            download_folder = '/home/desarrollo-02/Descargas/'
            
            # Create the download directory if it doesn't exist
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)

            # formato  a descargar y calidad
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'restrictfilenames': True,
            }
            
            print(ydl_opts)
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=True)
                    video_title = info_dict.get('title', 'video')
                    video_filename = ydl.prepare_filename(info_dict)

                    # Return a file as a download response
                    response = HttpResponse(open(video_filename, 'rb'), content_type='application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(video_filename)}"'
                    return response
            except yt_dlp.utils.DownloadError as e:
                messages.error(request, f'An error occurred: {e}')
            except Exception as e:
                messages.error(request, f'An unexpected error occurred: {e}')
        
    else:
            print("error no puede descargar")
            
    return render(request, 'paginas/descargas.html')
    