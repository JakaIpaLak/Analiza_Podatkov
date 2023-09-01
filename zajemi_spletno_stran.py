import requests
import re

#razred za posamezno besedilo
class Besedilo:
    def __init__(self, html_raw="", html_blocks=""):
        self.html_raw=html_raw
        self.html_blocks=html_blocks

    #preberi spletno stran
    def read_website(self, web_link):
        ht=requests.get(web_link)
        self.html_raw+=ht.text

    #popravi in uredi besedilo na bloke za lažjo predelavo
    def make_blocks(self, pattern):
        block_list=re.findall(pattern, self.html_raw)
        self.html_blocks+="\n\n".join(block_list)
    def clean_text(self):
        self.html_blocks=self.html_blocks.replace("&nbsp;", " ")
    	
    #shrani original oz. bloke
    def save_rawhtml(self, file_name):
        with open(file_name, "wb") as f: f.write(self.html_raw.encode())
    def save_blocks(self, file_name):
        with open(file_name, "wb") as f: f.write(self.html_blocks.encode())