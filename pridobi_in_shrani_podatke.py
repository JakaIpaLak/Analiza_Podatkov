import re
import csv

#razred za pridobivanje podatkov
class Podatki:
    def __init__(self):
        self.data_dict={}
        self.data_list=[]

    #najdi podatke 
    def find_data(self, text, pattern, data_name): #regex vzorec iskanih podatkov podan v slovarju {ime podatka : vzorec}
        find_list=re.findall(pattern, text)
        if(len(self.data_list)==0): 
            for n in find_list: self.data_list.append({data_name : n}) 
        else: 
            for n in range(len(find_list)): self.data_list[n][data_name] = find_list[n]
        self.data_dict[data_name] = find_list.copy()
    def find_data_no_dict(self, text, pattern): #regex vzorec iskanih podatkov podan s imeni grup  (?P<ime podatka>)
        find_list=re.finditer(pattern, text)
        m=0
        for iter in find_list: 
            self.data_list[m].update(iter.groupdict())
            m+=1
    
    #shrani podatke v csv datoteko
    def save_data(self, file_name): 
        with(open(file_name, "w", newline="")) as f:
            write=csv.DictWriter(f, fieldnames=list(self.data_list[0].keys()))
            write.writeheader()
            write.writerows(list(self.data_list))