import os
from dotenv import load_dotenv
import logging
load_dotenv()
import json
from logs_cfg import config_logger
config_logger()
currentPath = os.getcwd()
logger = logging.getLogger(__name__)
from aia_utils.img_utils import ImageUtils

#poetry run pytest tests/test_img.py::test_html2img -s
def test_html2img():
    #from html2image import Html2Image
    #hti = Html2Image(output_path='target')
    hti = ImageUtils(output_path='target')
    #open text file in read mode
    text_file = open("resources/test/demofile2.html", "r")
    css_file = open("resources/test/wahapedia.css", "r")
    
    #read whole file to a string
    data = text_file.read()
    
    #close file
    text_file.close()
    
    print(data)


    #html = '<h1> A title </h1> Some text.'
    #css = 'body {background: yellow;}'
    css =  css_file.read()
    css_file.close()

    # screenshot an HTML string (css is optional)
    image = hti.html2img(name='page3.png', html=data, css=css, size=(1100, 1200))
    logger.debug(f"width: {image.width} height: {image.height}")
    #image.show()
    assert(image.width == 2200 and image.height == 2400)
    #hti.screenshot(html_str=data, css_str=css, save_as='page3.png', size=(1100, 1400))

    #hti.screenshot(url='https://wahapedia.ru/wh40k10ed/factions/space-marines/Tactical-Squad#google_vignette', 
    #               save_as='wahapedia2.png')