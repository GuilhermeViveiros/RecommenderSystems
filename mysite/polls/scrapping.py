import selenium
from selenium import webdriver
import os
import time
import hashlib
import io
from PIL import Image
import requests

# This is the path I use
# DRIVER_PATH = '.../Desktop/Scraping/chromedriver 2'
# Put the path for your ChromeDriver here
DRIVER_PATH = './chromedriver'
wd = webdriver.Chrome(executable_path=DRIVER_PATH)


#query : Search term, like Dog
#max_links_to_fetch : Number of links the scraper is supposed to collect
#webdriver : instantiated Webdriver
def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    max_links_to_fetch = 1
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    #search_url = "https://www.imdb.com/title/tt0068732/?ref_=rvi_tt"
    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while (image_count < max_links_to_fetch and not number_results==0):
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.rg_ic")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        
        
        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls    
            actual_images = wd.find_elements_by_css_selector('img.irc_mi')
            for actual_image in actual_images:
                if actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

                image_count = len(image_urls)

                if len(image_urls) >= max_links_to_fetch:
                    print(f"Found: {len(image_urls)} image links, done!")
                    break
            else:
                print("Found:", len(image_urls), "image links, looking for more ...")
                time.sleep(1)
                load_more_button = wd.find_element_by_css_selector(".ksb")
                if load_more_button:
                    wd.execute_script("document.querySelector('.ksb').click();")

            # move the result startpoint further down
            results_start = len(thumbnail_results)

    return image_urls

#The persist_image function grabs an image URL url and downloads it into the folder_path. 
#The function will assign the image a random 10-digit id.
def persist_image(folder_path:str,url:str,search_term):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        if(not os.path.exists(folder_path+search_term+'jpg')):
            file_path = os.path.join(folder_path,search_term + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

def search_and_download(search_term:str,driver_path:str,target_path='./images',number_images=1):
    
    target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))
    print(target_folder)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)
        
    for elem in res:
        persist_image(target_folder,elem,search_term)


def scrap_image(movie):

    search_and_download(
        search_term=movie,
        driver_path=DRIVER_PATH
    )