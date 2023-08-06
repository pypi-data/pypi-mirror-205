"""这是一个封装YS SN号 CSV表格的操作接口的模块。
它依赖软件包 numpy。
"""

import json
import numpy as np
import logging

class SNCSVTableWrapper(object):
    """Note
    """
    def __init__(self, csv_file):
        self._logger = logging.getLogger(__name__)
        self._csv_file = csv_file
        self._array = None
    
    def _convert_csv_to_ndarray(self):
        try:
            with open(self._csv_file, 'r', encoding='utf-8') as f:
                self._array = np.genfromtxt(f, skip_header=2, delimiter=',', autostrip=True, dtype='unicode')
                #print(repr(self._array))
        except Exception as e:
            print(e)
            self._array = None

    def get_long_qrcode(self, sn):
        self._convert_csv_to_ndarray()
        if self._array is not None:
            index = (self._array == sn)
            #print(repr(index))
            index1 = np.nonzero(index)
            #print(repr(index1))
            if index1[0].size > 0 and index1[1].size > 0:
                x = self._array[index1[0], index1[1]+1]
                #print(repr(x))
                #print(x[0])
                return x[0]
        
        return None

    def get_sn(self, long_qrcode):
        self._convert_csv_to_ndarray()
        if self._array is not None:
            index = (self._array == long_qrcode)
            #print(repr(index))
            index1 = np.nonzero(index)
            #print(repr(index1))
            if index1[0].size > 0 and index1[1].size > 0:
                x = self._array[index1[0], index1[1]-1]
                #print(repr(x))
                #print(x[0])
                return x[0]
        
        return None
    
    def find_sn_and_long_qrcode(self, sn, long_qrcode):
        return self.get_sn(long_qrcode) == sn

if __name__ == "__main__":
    
    file = '23年第1批eMan_SN及长码.csv'
    table = SNCSVTableWrapper(file)

    long = ['oX1Sjj+cy08zXRRtv1o7ruoEdk/0AGtK','elfG42zSbuethXdnbn3Hj0lCjAwIFXjl','Fenq8qIlxRFMS6kDqJc/MvOvY+t15wK/','sGHKSxke/jkQrItY/kS83uACqT/NC7Uc']
    for i in long:
        print(table.get_sn(i))

    sn = ['YSEM1010R012301A0001','YSEM1010R012301A0002','YSEM1010R012301A0008','YSEM1010R012301A0009']
    for i in sn:
        print(table.get_long_qrcode(i))
        
    print(table.find_sn_and_long_qrcode('YSEM1010R012301A0001', 'oX1Sjj+cy08zXRRtv1o7ruoEdk/0AGtL'))
    print(table.find_sn_and_long_qrcode('YSEM1010R012301A0009', 'sGHKSxke/jkQrItY/kS83uACqT/NC7Ud'))

    print(table.find_sn_and_long_qrcode('YSEM1010R012301A0100', 'oX1Sjj+cy08zXRRtv1o7ruoEdk/0AGtL'))
    print(table.find_sn_and_long_qrcode('YSEM1010R012301A0101', 'sGHKSxke/jkQrItY/kS83uACqT/NC7Ud'))

    print(table.find_sn_and_long_qrcode('YSEM1010R012301A0001', 'oX1Sjj+cy08zXRRtv1o7ruoEdk/0AGtK'))
    print(table.find_sn_and_long_qrcode('YSEM1010R012301A0009', 'sGHKSxke/jkQrItY/kS83uACqT/NC7Uc'))