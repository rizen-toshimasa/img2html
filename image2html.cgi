#!"C:\Python27\python.exe"
#coding: utf-8
import cgi
import cgitb
import sys
import os
import cv2
import numpy
from StringIO import StringIO

def img2html(img,mark):
    html = u''
    test =  [flatten for inner in img for flatten in inner]#１次元配列にする
    for i,pix in enumerate(test):
        if (i+1)%16 == 0:
            br = u'<br>'
        else:
            br = u''
        if i == 0:
            html += u'<font color="'
            html += u'#%02X%02X%02X' % (pix[2],pix[1],pix[0])
            html += u'">'
            html += mark
        elif all(test[i]==test[i-1]):
            html += mark
            html += br
        else:
            html += u'</font>'
            html += br
            html += u'<font color="'
            html += u'#%02X%02X%02X' % (pix[2],pix[1],pix[0])
            html += u'">'
            html += mark
    html += u'</font>'
    return html
def data2img(data):
    pass
if __name__ == '__main__':
    html = u'''Content-Type: text/html\n
<!Doctype html>
<html lang="ja">
<head>
    <meta charset="utf-8">
    <title>画像2html</title>
    <link rel="stylesheet" href="css/default.css">
    <style>
    body{
        font-family: 'ヒラギノ角ゴ Pro W3',
        'Hiragino Kaku Gothic Pro','メイリオ',
        Meiryo,'ＭＳ Ｐゴシック',sans-serif;
    }
    </style>
</head>
<body>
    <h2>画像をhtmlにする</h2>
    %s
    <form action="image2html.cgi" method="post" enctype="multipart/form-data">
      <input type="file" name="file" id="file" value=""/>
      <input type="submit" id="btn-upload" value="Upload Image..." />
    </form>
</body>
</html>'''
    try:
        import msvcrt
        msvcrt.setmode(0, os.O_BINARY)
        msvcrt.setmode(1, os.O_BINARY)
    except ImportError:
        pass


    f = open("F:\www\python\hoge.png", "rb")
    rawImage = f.read()
    test = numpy.asarray(bytearray(rawImage),dtype=numpy.uint8)
    img =  cv2.imdecode(test,1)

    form = cgi.FieldStorage()
    if form.has_key('file') and (form["file"].value !=''):
        data = form["file"].file.read(1000)
        if not data:
            break
        test = numpy.asarray(bytearray(data),dtype=numpy.uint8)
        img = cv2.imdecode(test,1)


    colorHtml = img2html(img,u'█ ')
    html = html % colorHtml
    print html.encode('utf8')