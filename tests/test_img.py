import os
from dotenv import load_dotenv
import logging
load_dotenv()
import json
from logs_cfg import config_logger
config_logger()
currentPath = os.getcwd()
logger = logging.getLogger(__name__)


#poetry run pytest tests/test_img.py::test_html2img -s
def test_html2img():
    from html2image import Html2Image
    hti = Html2Image(output_path='target')
    #open text file in read mode
    text_file = open("resources/demofile2.html", "r")
    
    #read whole file to a string
    data = text_file.read()
    
    #close file
    text_file.close()
    
    print(data)


    html = '<h1> A title </h1> Some text.'
    css = 'body {background: yellow;}'

    # screenshot an HTML string (css is optional)
    #hti.screenshot(html_str=data, css_str=css, save_as='page2.png')

    hti.screenshot(url='https://wahapedia.ru/wh40k10ed/factions/space-marines/Tactical-Squad#google_vignette', 
                   save_as='wahapedia2.png')