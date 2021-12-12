import mimetypes
import re
import time
import datetime as dt



def formato_iso_para_br(data: str) -> str:
        '''
        Formato da data de entrada 'yyyy-mm-dd'
        '''
        if type(data) != type("string"):
            return data
        if not re.match(r"(\d{4})[-.\/](\d{2})[-.\/](\d{2})", data):
            return data
        date = dt.datetime.strptime(data, '%Y-%m-%d')
        string_date_formato_br = dt.datetime.strftime(date, format='%d/%m/%Y')
        return string_date_formato_br


def formato_br_para_iso(data: str) -> str:
    '''
    Formato da data de entrada 'dd/mm/yyyy'
    '''
    ##Regex que válida até ano bissexto para o formato acima##
    pattern = r"""(^(((0[1-9]|1[0-9]|2[0-8])[\/](0[1-9]|1[012]))|\
        ((29|30|31)[\/](0[13578]|1[02]))|((29|30)[\/](0[4,6,9]|11)))[\/]\
        (19|[2-9][0-9])\d\d$)|(^29[\/]02[\/](19|[2-9][0-9])(00|04|08|12|16|20|\
        24|28|32|36|40|44|48|52|56|60|64|68|72|76|80|84|88|92|96)$)
        """
    if type(data) != type("string"):
        return data
    if not re.match(pattern, data):
        return data
    date = dt.datetime.strptime(data, '%d/%m/%Y')
    string_date_formato_iso = dt.datetime.strftime(date, format="%Y-%m-%d")
    return string_date_formato_iso


def compara_datas(data, data2):
    """
    Compara duas datas de forma a comparar se a primeira data passada como parametro
    é maior que a segunda data passada como parametro. Serve para ver qual data está vencida
    """
    date1 = time.strptime(data, "%d/%m/%Y")
    date2 = time.strptime(data2, "%d/%m/%Y")
    return date1 > date2
    

def compara_datas2(data, data2):
    """
    Compara duas datas de forma a comparar se a primeira data passada como parametro
    é maior que a segunda data passada como parametro. Serve para ver qual data não esta vencida
    """
    date1 = time.strptime(data, "%d/%m/%Y")
    date2 = time.strptime(data2, "%d/%m/%Y")
    return date1 < date2
    
    
def advinha_tipo_arquivo(attachmentFile: str) -> str:
    content_type, encoding = mimetypes.guess_type(attachmentFile)
    try:
        file = attachmentFile.split('/')[-1]
        if ".PDF" in file.upper():
            return "pdf"
        if ".XLSX" in file.upper():
            return "excel"
        if ".PY" in file.upper():
            return "python"
    except:
        pass
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(attachmentFile, 'rb')
        msg = "text"
        fp.close()
    elif main_type == 'image':
        fp = open(attachmentFile, 'rb')
        msg = "image"
        fp.close()
    elif main_type == 'audio':
        fp = open(attachmentFile, 'rb')
        msg = "audio"
        fp.close()
    else:
        fp = open(attachmentFile, 'rb')
        msg = "arquivo"
        fp.close()
    return msg

if __name__ == '__main__':
    print(formato_br_para_iso("10/11/2029"))