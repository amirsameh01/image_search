
from uuid import uuid4
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from PIL import Image
from django.conf import settings
from .models import FinalImages
import io
import time
import requests
import base64
import os

class ImageScraper():
    
    def __init__(self):
        options = ChromeOptions() 
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        
    def setup(self, search_param):
        url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={s}&oq={s}&gs_l=img"
        self.driver.get(url.format(s=search_param)) 


    def get_images(self, search_param, image_count):
        
        # Selenium logic to search and download images
        # Returns list of images
        self.setup(search_param)
        
        image_urls = []
        num_downloaded = 0
    
        while num_downloaded < image_count:

            # Scroll to end of page 
            self.scroll_to_end()

            # Get images 
            images = self.driver.find_elements(By.CSS_SELECTOR, "img.rg_i.Q4LuWd")
            
            for img in images:
                src = img.get_attribute("src")
                image_urls.append(src)
                
                num_downloaded += 1
                if num_downloaded == image_count:
                    break

        return image_urls

    def scroll_to_end(self):

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for page to load
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break

            last_height = new_height
        time.sleep(0.5)
        
    def resize_images(self, image_urls):  
        
        resized_images = []
        for src in image_urls:  
            if src.startswith('data:'):
                # Base64 decode and resize
                image_data = src.split(',')[1]
                image_bytes = base64.b64decode(image_data)  
                img = Image.open(io.BytesIO(image_bytes))
            

            else:
                # Direct link - download and resize
                response = requests.get(src)   
                img = Image.open(io.BytesIO(response.content))


            # Resize image
            resized_img = img.resize(settings.RESIZE_SCALES)
            buffered = io.BytesIO()
            resized_img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            resized_images.append(img_str)

        return list(resized_images)


    def save_images(self, image_data):
          
          for img_data in image_data:
                image_bytes = base64.b64decode(img_data)
                            
                # Write image file
                image_name = f'image_{uuid4()}.jpg'
                image_path = os.path.join(settings.MEDIA_ROOT, image_name)
                with open(image_path, 'wb') as f:
                    f.write(image_bytes)

            #Saving image to db
                final_img = FinalImages(file=image_name)
                final_img.save()