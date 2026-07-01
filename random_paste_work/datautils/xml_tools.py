import os
from lxml import etree
from typing import List,Union

__all__ = ['ReadAnnotation','write2xml']


class ReadAnnotation():
    """
    读取voc数据集中，xml标注数据
    """

    def __init__(self, file_path: str):
        super(ReadAnnotation, self).__init__()
        self._file_path = file_path
        try:

            self._root = etree.parse(self._file_path).getroot()
        except Exception as e:
            print(e)
            exit(0)


        self._img_width = self._root.xpath('//width')[0].text
        self._img_height = self._root.xpath('//height')[0].text
        # 读取所有原bndbox信息，下面5项都是list
        self._xmin = self._root.xpath('//bndbox/xmin/text()')
        self._ymin = self._root.xpath('//bndbox/ymin/text()')
        self._xmax = self._root.xpath('//bndbox/xmax/text()')
        self._ymax = self._root.xpath('//bndbox/ymax/text()')
        self._cls_names = self._root.xpath('//object/name/text()')
        self._score = self._root.xpath('//object/score/text()')

        self._file_name = self._root.xpath('//filename/text()')[0]

    @property
    def width(self):
        return int(self._img_width)

    @property
    def height(self):
        return int(self._img_height)

    @property
    def file_name(self):
        return self._file_name

    def get_ann(self):
        for x1, y1, x2, y2, cls_name, score in zip(self._xmin, self._ymin, self._xmax, self._ymax, self._cls_names, self._score):
            yield float(x1), float(y1), float(x2), float(y2), cls_name, float(score)

    def count_bbox(self):
        return len(self._root.xpath('//object/name/text()'))

    def write2xml(self, img_w: int, img_h: int, bboxes: List[List[Union[int, str]]], target_file: str):
        """
        重新写一个xml文件
        :param img_w:
        :param img_h:
        :param bboxes: [[xmin,ymin,xmax,ymax,cls_name]]
        :param target_file:
        :return:
        """

        ann = etree.Element('annotation')
        folder = etree.SubElement(ann,'folder')
        filename = etree.SubElement(ann,'filename')
        filename.text = self.file_name
        path = etree.SubElement(ann,'path')
        source = etree.SubElement(ann,'source')
        database = etree.SubElement(source,'database')
        database.text = 'Unknown'
        size = etree.SubElement(ann,'size')
        width = etree.SubElement(size,'width')
        width.text = str(img_w)
        height = etree.SubElement(size,'height')
        height.text = str(img_h)
        depth = etree.SubElement(size,'depth')
        depth.text = '3'

        segmented = etree.SubElement(ann,'segmented')
        segmented.text = '0'

        for xmin,ymin,xmax,ymax,cls_name in bboxes:
            object = etree.SubElement(ann, 'object')
            name = etree.SubElement(object, 'name')
            name.text = cls_name
            pose = etree.SubElement(object, 'pose')
            pose.text = 'Unspecified'
            truncated = etree.SubElement(object, 'truncated')
            truncated.text = '0'
            difficult = etree.SubElement(object, 'difficult')
            difficult.text = '0'
            bndbox = etree.SubElement(object, 'bndbox')
            _xmin = etree.SubElement(bndbox, 'xmin')
            _xmin.text = str(int(xmin))
            _ymin = etree.SubElement(bndbox, 'ymin')
            _ymin.text = str(int(ymin))
            _xmax = etree.SubElement(bndbox, 'xmax')
            _xmax.text = str(int(xmax))
            _ymax = etree.SubElement(bndbox, 'ymax')
            _ymax.text = str(int(ymax))
        tree = etree.ElementTree(ann)
        tree.write(target_file, pretty_print=True, xml_declaration=True, encoding='utf-8')

def write2xml(img_w: int, img_h: int, bboxes: List[List[Union[int, str]]], target_file: str):
    """
    重新写一个xml文件
    :param img_w:
    :param img_h:
    :param bboxes: [[xmin,ymin,xmax,ymax,cls_name]]
    :param target_file:
    :return:
    """

    ann = etree.Element('annotation')
    folder = etree.SubElement(ann, 'folder')
    filename = etree.SubElement(ann, 'filename')
    filename.text = os.path.basename(target_file)[:-4] + '.jpg'
    path = etree.SubElement(ann, 'path')
    source = etree.SubElement(ann, 'source')
    database = etree.SubElement(source, 'database')
    database.text = 'Unknown'
    size = etree.SubElement(ann, 'size')
    width = etree.SubElement(size, 'width')
    width.text = str(img_w)
    height = etree.SubElement(size, 'height')
    height.text = str(img_h)
    depth = etree.SubElement(size, 'depth')
    depth.text = '3'

    segmented = etree.SubElement(ann, 'segmented')
    segmented.text = '0'

    for xmin, ymin, xmax, ymax, cls_name in bboxes:
        object = etree.SubElement(ann, 'object')
        name = etree.SubElement(object, 'name')
        name.text = cls_name
        pose = etree.SubElement(object, 'pose')
        pose.text = 'Unspecified'
        truncated = etree.SubElement(object, 'truncated')
        truncated.text = '0'
        difficult = etree.SubElement(object, 'difficult')
        difficult.text = '0'
        bndbox = etree.SubElement(object, 'bndbox')
        _xmin = etree.SubElement(bndbox, 'xmin')
        _xmin.text = str(int(xmin))
        _ymin = etree.SubElement(bndbox, 'ymin')
        _ymin.text = str(int(ymin))
        _xmax = etree.SubElement(bndbox, 'xmax')
        _xmax.text = str(int(xmax))
        _ymax = etree.SubElement(bndbox, 'ymax')
        _ymax.text = str(int(ymax))
    tree = etree.ElementTree(ann)
    tree.write(target_file, pretty_print=True, xml_declaration=True, encoding='utf-8')
if __name__ == '__main__':
    r = ReadAnnotation(r'E:\yaoteam\hanxiaotong_data\train\1.5x\2013-01-01_12-10-52_0.xml')

    # for x1,y1,x2,y2,cls_name in r.get_ann():
    #     print(f"x1:{x1},y1:{y1},x2:{x2},y2:{y2},cls:{cls_name}")
    r.write2xml(100,200,[[1,2,3,4,'kk'],[23,45,67,89,'jj']], target_file=r'E:\yaoteam\hanxiaotong_data\train\1.5x\111.xml')
    print(r.count_bbox())
