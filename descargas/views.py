import os
from django.shortcuts import render, redirect
import yt_dlp
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

def video(request):
    """
    Renders the main video download page.
    """
    return render(request, 'paginas/descargas.html')

import os
import yt_dlp
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect  # Opcional, para redirects más limpios

def download_video(request):
    if request.method == 'POST':
        video_url = request.POST.get('url')
        format_choice = request.POST.get('format')  # 'mp4' o 'mp3' del radio button
        
        if not video_url:
            messages.error(request, "Por favor, ingresa una URL válida.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        download_folder = os.path.join(os.getcwd(), 'downloads')  # Ajusta tu carpeta
        os.makedirs(download_folder, exist_ok=True)  # Crea la carpeta si no existe
        
        if format_choice == 'mp4':
            Mp4 = {
                'format': 'best[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'restrictfilenames': True,
                'noplaylist': True,  # Solo descarga el video individual
            }
            ydl_opts = Mp4
            content_type = 'video/mp4'
            
        elif format_choice == 'mp3':
            Mp3 = {
                'format': 'bestaudio/best',  # Solo audio de mejor calidad
                'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
                'restrictfilenames': True,
                'noplaylist': True,
                # Postprocesador para extraer y convertir a MP3
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',  # Calidad de audio (192kbps, ajusta si quieres)
                }],
            }
            ydl_opts = Mp3
            content_type = 'audio/mpeg'
            
        else:
            messages.error(request, "Formato no válido seleccionado.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
      
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                video_filename = ydl.prepare_filename(info_dict)
                
                # Si es MP3, el nombre podría cambiar por el postprocesador (agrega .mp3 si no lo tiene)
                if format_choice == 'mp3' and not video_filename.endswith('.mp3'):
                    video_filename = video_filename.rsplit('.', 1)[0] + '.mp3'
                
                # Verifica que el archivo existe después de la descarga
                if not os.path.exists(video_filename):
                    raise Exception("El archivo no se descargó correctamente.")
                
                # Abre y envía el archivo
                with open(video_filename, 'rb') as f:
                    response = HttpResponse(f.read(), content_type=content_type)
                    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(video_filename)}"'
                    messages.success(request,f"Descarga exitosa")  # Para logs
                    return response
            
                
        except yt_dlp.utils.DownloadError as e:
            messages.error(request, f'Ocurrió un error al descargar el video: {str(e)[:100]}...') 
        except Exception as e:
            messages.error(request, f'Ocurrió un error inesperado: {str(e)}')
    
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
