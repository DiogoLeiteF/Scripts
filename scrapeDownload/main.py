import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import requests
import io
from PIL import Image

wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wd.get("https://www.google.com")

image_url = "https://icatcare.org/app/uploads/2018/07/Thinking-of-getting-a-cat.png"


def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = 'https://www.google.com/search?q=cats&&tbm=isch&ved=2ahUKEwinu6nNkfn5AhXaRPEDHXBdC4sQ2-cCegQIABAA&oq=cats&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIECAAQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIECAAQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgARQAFgAYNG0whVoAXAAeACAAcsCiAHLApIBAzMtMZgBAKoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=fI0TY6eNJNqJxc8P8Lqt2Ag&bih=919&biw=1920'
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, 'Q4LuWd')

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue
            images = wd.find_elements(By.CLASS_NAME, 'n3VNCb')
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f'Found image! -> {len(image_urls)}')

    return image_urls


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, 'wb') as f:
            image.save(f, 'JPEG')

        print("Success")
    except Exception as e:
        print('Failed: ', e)


# download_image("", image_url, 'test.jpg')
urls = get_images_from_google(wd, 1, 7)
print(urls)

for i, url in enumerate(urls):
    download_image('img/', url, str(i)+'.jpg')


wd.quit()
