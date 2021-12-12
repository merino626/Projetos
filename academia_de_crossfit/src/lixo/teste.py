import datetime as dt
import time
import re

### De ISO para formato BR ###
def formato_iso_para_br(data) -> str:
    '''
    Formato da data de entrada 'yyyy-mm-dd'
    '''
    if not re.match("(\d{4})[-.\/](\d{2})[-.\/](\d{2})", data):
        return "data invalida"
    date = dt.datetime.strptime(data, '%Y-%m-%d')
    string_date_formato_br = dt.datetime.strftime(date, format='%d/%m/%Y')
    return string_date_formato_br

### Formato BR para ISO ###
def formato_br_para_iso(data) -> str:
    '''
    Formato da data de entrada 'dd/mm/yyyy'
    '''
    ##Regex que válida até ano bissexto para o formato acima##
    pattern = """(^(((0[1-9]|1[0-9]|2[0-8])[\/](0[1-9]|1[012]))|\
        ((29|30|31)[\/](0[13578]|1[02]))|((29|30)[\/](0[4,6,9]|11)))[\/]\
        (19|[2-9][0-9])\d\d$)|(^29[\/]02[\/](19|[2-9][0-9])(00|04|08|12|16|20|\
        24|28|32|36|40|44|48|52|56|60|64|68|72|76|80|84|88|92|96)$)
"""
    
    if not re.match(pattern, data):
        return data
    date = dt.datetime.strptime(data, '%d/%m/%Y')
    string_date_formato_iso = dt.datetime.strftime(date, format="%Y-%m-%d")
    return string_date_formato_iso


#print(formato_br_para_iso("05/10/200"))

def compara_datas(data, data2):
    date1 = time.strptime(data, "%d/%m/%Y")
    date2 = time.strptime(data2, "%d/%m/%Y")
    return date1 > date2

#compara_datas("14/10/2021", "14/10/2021")


compara_datas(formato_iso_para_br((str(dt.datetime.now().date()))), "12/10/2021")
