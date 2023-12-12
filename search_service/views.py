from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from rest_framework.views import APIView  
from .img_tools import ImageScraper


class ImageFinder(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request):
        
        search_param = request.POST.get('stext')
        image_count = int(request.POST.get('scount', 5))
        
        # Create scraper instance
        scraper = ImageScraper()  
        
        # Call methods on instance 
        images_urls = scraper.get_images(search_param, image_count)
        
        # # Resize
        resized_images = scraper.resize_images(images_urls)

        # # Save 
        saved_paths = scraper.save_images(resized_images)

        return JsonResponse({'message': 'Images has been downloaded, resized and saved'})

        