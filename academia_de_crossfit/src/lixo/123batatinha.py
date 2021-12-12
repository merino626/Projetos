import mimetypes



content_type, encoding = mimetypes.guess_type("Manual_NFe_v401_2009-11-04.pdf")
print(content_type, encoding)