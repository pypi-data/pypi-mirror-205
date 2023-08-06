# BadgeScale_YS_PLT

#### 介绍
badgescale-ys-plt 全称是 badge scale yunsi production line tool，解释是 专门针对云思工牌整机的生产测试工具，工作在上位机PC Windows上。

#### 软件架构
软件架构说明


#### 安装教程

1.  xxxx
2.  xxxx
3.  xxxx

#### 使用说明

1.  xxxx
2.  xxxx
3.  xxxx

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)

#### BLE协议相关

2023-04-25 16:03:17,123 __main__ INFO: starting scan...
2023-04-25 16:03:17,663 __main__ INFO: connecting to device...
2023-04-25 16:03:21,229 __main__ INFO: connected
2023-04-25 16:03:21,230 __main__ INFO: [Service] 00001800-0000-1000-8000-00805f9b34fb (Handle: 1): Generic Access Profile
2023-04-25 16:03:21,345 __main__ INFO:   [Characteristic] 00002a00-0000-1000-8000-00805f9b34fb (Handle: 2): Device Name (read), Value: bytearray(b'EM-0023-0001')
2023-04-25 16:03:21,646 __main__ INFO:   [Characteristic] 00002a01-0000-1000-8000-00805f9b34fb (Handle: 4): Appearance (read), Value: bytearray(b'\xd8\x02')
2023-04-25 16:03:21,770 __main__ INFO:   [Characteristic] 00002ac9-0000-1000-8000-00805f9b34fb (Handle: 6): Resolvable Private Address Only (read), Value: bytearray(b'')
2023-04-25 16:03:21,771 __main__ INFO: [Service] 00001801-0000-1000-8000-00805f9b34fb (Handle: 8): Generic Attribute Profile
2023-04-25 16:03:21,772 __main__ INFO:   [Characteristic] 00002a05-0000-1000-8000-00805f9b34fb (Handle: 9): Service Changed (indicate)
2023-04-25 16:03:21,885 __main__ INFO:     [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 11): Client Characteristic Configuration, Value: bytearray(b'\x02\x00')
2023-04-25 16:03:22,006 __main__ INFO:   [Characteristic] 00002b29-0000-1000-8000-00805f9b34fb (Handle: 12): Client Supported Features (read,write), Value: bytearray(b'\x01')
2023-04-25 16:03:22,126 __main__ INFO:   [Characteristic] 00002b2a-0000-1000-8000-00805f9b34fb (Handle: 14): Database Hash (read), Value: bytearray(b'\x04\xab\xf2\xfcv\x9cy\xc3\x84\xdbD<\xe4Z\xfe\xb7')
2023-04-25 16:03:22,127 __main__ INFO: [Service] 0000fee0-0000-1000-8000-00805f9b34fb (Handle: 16): Anhui Huami Information Technology Co.
2023-04-25 16:03:22,246 __main__ INFO:   [Characteristic] 0000fee1-0000-1000-8000-00805f9b34fb (Handle: 17): fee1_only_read (read), Value: bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
2023-04-25 16:03:22,426 __main__ INFO:     [Descriptor] 00002901-0000-1000-8000-00805f9b34fb (Handle: 19): Characteristic User Description, Value: bytearray(b'fee1_only_read')2023-04-25 16:03:22,426 __main__ INFO:   [Characteristic] 0000fee2-0000-1000-8000-00805f9b34fb (Handle: 20): Anki: Inc. (write-without-response)
2023-04-25 16:03:22,427 __main__ INFO:   [Characteristic] 0000fee3-0000-1000-8000-00805f9b34fb (Handle: 22): Anki: Inc. (write)
2023-04-25 16:03:22,427 __main__ INFO:   [Characteristic] 0000fee4-0000-1000-8000-00805f9b34fb (Handle: 24): Nordic Semiconductor ASA (notify)
2023-04-25 16:03:22,545 __main__ INFO:     [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 26): Client Characteristic Configuration, Value: bytearray(b'\x00\x00')
2023-04-25 16:03:22,546 __main__ INFO:   [Characteristic] 0000fee5-0000-1000-8000-00805f9b34fb (Handle: 27): Nordic Semiconductor ASA (indicate)
2023-04-25 16:03:22,666 __main__ INFO:     [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 29): Client Characteristic Configuration, Value: bytearray(b'\x00\x00')
2023-04-25 16:03:22,667 __main__ INFO: [Service] f000ffc0-0451-4000-b000-000000000000 (Handle: 30): Unknown
2023-04-25 16:03:22,667 __main__ INFO:   [Characteristic] f000ffc1-0451-4000-b000-000000000000 (Handle: 31): Unknown (write-without-response)
2023-04-25 16:03:22,668 __main__ INFO:   [Characteristic] f000ffc2-0451-4000-b000-000000000000 (Handle: 33): Unknown (notify)
2023-04-25 16:03:22,846 __main__ INFO:     [Descriptor] 00002902-0000-1000-8000-00805f9b34fb (Handle: 35): Client Characteristic Configuration, Value: bytearray(b'\x00\x00')
2023-04-25 16:03:22,846 __main__ INFO: disconnecting...
2023-04-25 16:03:37,788 __main__ INFO: disconnected


class DevicePairingKinds(enum.IntFlag):
    NONE = 0
    CONFIRM_ONLY = 0x1
    DISPLAY_PIN = 0x2
    PROVIDE_PIN = 0x4
    CONFIRM_PIN_MATCH = 0x8
    PROVIDE_PASSWORD_CREDENTIAL = 0x10


UUID:0000fee4-0000-1000-8000-00805f9b34fb
Properties:NOTIFY

<!-- UUID:0000fee2-0000-1000-8000-00805f9b34fb
Properties:WRITE NO RESPONSE -->

UUID:0000fee3-0000-1000-8000-00805f9b34fb
Properties:WRITE

#### QR扫描相关

逊镭 NTEUMM L6
vid=0x17ef, pid=0x608c


#### pysimplegui相关

Theme Name Format
You can look at the table of available themes to get the name of a theme you want to try, or you can "guess" at one using this formula:

<"Dark" | "Light"> <Color> [#]

Where Color is one of these:

Black, Blue, Green, Teal, Brown, Yellow, Gray, Purple

The # is optional and is used when there is more than 1 choice for a color. For example, for "Dark Blue" there are 12 different themes (Dark Blue, and Dark Blue 1-11). These colors specify the rough color of the background. These can vary wildly so you'll have to try them out to see what you like the best.