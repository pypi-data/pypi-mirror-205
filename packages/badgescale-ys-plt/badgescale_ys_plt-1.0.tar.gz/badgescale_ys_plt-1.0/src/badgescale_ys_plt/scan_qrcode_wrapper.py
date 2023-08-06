"""这是一个封装扫描二维码接口的模块。
它依赖软件包 pywinusb。
基于作者jakey.chen的 hidHelper进行修改，感谢作者jakey.chen
"""

'''
win下使用的HID设备通讯帮助类
'''
__author__ = "jakey.chen"
__version__ = "v1.0"

import pywinusb.hid as hid
import queue

class ScanQRCodeWrapper(object):

    def __init__(self, vid=0x1391, pid=0x2111):
        self.alive = False
        self.device = None
        self.report = None
        self.vid = vid
        self.pid = pid
        self.read_queue = queue.Queue(0)
        
    def start(self):
        '''
        开始，打开HID设备
        '''
        _filter = hid.HidDeviceFilter(vendor_id=self.vid, product_id=self.pid)
        hid_device = _filter.get_devices()
        if len(hid_device) > 0:
            #self.device = hid_device[0]
            self.device = hid_device[1]
            self.device.open()
            self.report = self.device.find_output_reports()
            self.alive = True
        if self.alive:
            self.setcallback()

    def stop(self):
        '''
        停止，关闭HID设备
        '''
        self.alive = False
        if self.device:
            self.device.close()

    def setcallback(self):
        '''
        设置接收数据回调函数
        '''
        if self.device:
            self.device.set_raw_data_handler(self.read)

    def read(self, data):
        '''
        接收数据回调函数
        '''
        #print([hex(item).upper() for item in data[1:]])
        self.read_queue.put(str(data[1:], encoding='utf-8'))

    def read_nonblock(self):
        '''读取设备前检测hid设备，若断开后，自动检测并尝试重连'''
        if not self.device.is_plugged():
            self.stop()
            self.start()
        
        try:
            str_data = self.read_queue.get(block=False)
        except Exception as e:
            return ''

        return str_data

    def write(self, send_list):
        '''
        向HID设备发送数据
        '''
        if self.device:
            if self.report:
                self.report[0].set_raw_data(send_list)
                bytes_num = self.report[0].send()
                return bytes_num

if __name__ == '__main__':
    ''''''
    myhid = ScanQRCodeWrapper(vid=0x17ef, pid=0x608c)
    myhid.start()
    
    for i in range(20):
        str_data = myhid.read_nonblock()
        print('qrcode:%s\n' % (str_data))
        import time
        time.sleep(0.5)
    
    myhid.stop()
