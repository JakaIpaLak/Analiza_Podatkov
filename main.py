import re
import os.path
from zajemi_spletno_stran import Besedilo
from pridobi_in_shrani_podatke import Podatki


#PRIDOBI BESEDILO
if os.path.isfile("Bloki.txt"): #Preveri če besedilo že obstaja
    while True:
        response = input("Ali želiš ponovno zajeti spletno stran?  Y/N  ")
        if response.lower() not in ["y", "n"]:
            print("Vnesi Y za ja oz. N na ne")
            continue
        else:
            if response.lower() == "y": preberi = True
            else: preberi = False
            break 
else: preberi = True


#Preberi besedilo in ga shrani
if preberi == True:
    b1 = Besedilo()
    for i in range(1, 275): b1.read_website("https://www.aviationfanatic.com/ent_list.php?ent=4&pg=" + str(i))

    pattern_block=re.compile(r'<th class="right">.+?<td class="right">.*?</td>', re.DOTALL)
    b1.make_blocks(pattern_block)
    b1.clean_text()

    while True: #shrani besedilo
        response = input("Ali želiš shraniti zajeto stran in pridobljene bloke besedila?  Y/N  ")
        if response.lower() not in ["y", "n"]:
            print("Vnesi Y za ja oz. N na ne")
            continue
        else:
            if response.lower() == "y": 
                b1.save_rawhtml("Cela_stran.txt")
                b1.save_blocks("Bloki.txt")
            break

with open("Bloki.txt", "r", errors='ignore') as f: html_blocks=f.read()


#PRIDOBI PODATKE
d1=Podatki()

#regex vzorci
pattern_dict={
    "Aircraft id" : r'<td><a href="ent_show.php\?ent=4&amp;AT_ID=(.+?)"',
    "Aircraft name" : r'<td class="mainname"><a href="ent_show.php\?ent=4&amp;AT_ID=.+?">(.+?)</a></td>',
    "Manufacturer" : r'<a href="ent_show.php\?ent=3&amp;MAN_ID=.+?">(.+?)</a></td>',
    "Country" : r'<a href="ent_list.php\?ent=4&amp;MAN_Country=.+?">(.+?)</a></td>',
}
pattern_other=re.compile(
    r'<td class="center">(?:|.+?">(?P<Category>.*?)<.+?)</td>.*?'
    r'<td class="center">(?:|.+?">(?P<Role>.*?)<.+?)</td>.*?'
    r'<td class="center">(?:|.+?">(?P<Engine_type>.*?)<.+?)</td>.*?'
    r'<td class="center">(?:|.+?">(?P<Engines>.*?)<.+?)</td>.*?'
    r'<td class="center">(?:|.+?">(?P<WTC>.*?)<.+?)</td>.*?'
    r'<td class="center">(?:|.+?">(?P<Seats>.*?)<.+?)</td>.*?'
    r'<td class="center">(?:|.+?">(?P<First_flight>.*?)<.+?)</td>.*?'
    r'<td class="center">(?:|.+?">(?P<Last_manufactured>.*?)<.+?)</td>.*?'
    r'<td class="right">(?:|(?P<Number_built>.+?))</td>',
    re.DOTALL
)

#poišči podatke
for i in pattern_dict:
    d1.find_data(html_blocks, re.compile(pattern_dict[i]), i)
d1.find_data_no_dict(html_blocks, pattern_other)

#shrni podatke
d1.save_data("Podatki.csv")