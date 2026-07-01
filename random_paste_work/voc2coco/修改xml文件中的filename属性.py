import os
import os.path
from xml.etree.ElementTree import parse, Element
 
# .xml文件地址
path = r"C:\Users\Windows\Desktop\yyc_python\voc2coco\VOC\Annotations"
# 得到文件夹下所有文件名称
files = os.listdir(path)
s = []
# 遍历文件夹
for xmlFile in files:
    # 判断是否是文件夹,不是文件夹才打开
    if not os.path.isdir(xmlFile):
        # print(xmlFile)
        pass
    path = r"C:\Users\Windows\Desktop\yyc_python\voc2coco\VOC\Annotations"
    newStr = os.path.join(path, xmlFile)
    #最核心的部分,路径拼接,输入的是具体路径
    #得到.xml文件的根（也就是annotation）
    dom = parse(newStr)
    root = dom.getroot()
    #获得后缀.前的文件名(分离文件名和扩展名)
    part = os.path.splitext(xmlFile)[0]
    # 文件名+后缀
    part1 = part + '.jpg'
    # path里的新属性值：
    # newStr1 = r'C:\Users\Windows\Desktop\yyc_python\voc2coco\VOC\JPEGImages'+ '\\' + part1
    # 通过句柄找到path的子节点，如果不存在则创建
    path_element = root.find('filename')
    if path_element is None:
        # 如果找不到 'path' 节点，则创建一个
        path_element = Element('filename')
        root.append(path_element)
    root.find('filename').text = part1
    # #打印输出
    print('已经修改')
    dom.write(newStr, xml_declaration=True)
    pass