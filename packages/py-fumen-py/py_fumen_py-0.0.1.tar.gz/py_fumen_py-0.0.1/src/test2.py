import py_fumen

data = 'v115@vhD3J2WAFLDmClcJSAVDEHBEooRBToAVB0/AAA3pB1?vBWyB'

pages = py_fumen.decoder.decode(data)
for i, page in enumerate(pages):
    print(i)
    print(page)

string = py_fumen.encoder.encode(pages)
print(data)
print(string)
