# bilibiliDan B站弹幕爬取工具

# 预览
![主界面](https://github.com/G1-kiyo/bilibiliDan/blob/master/static/preview.png)

## 功能
1. 弹幕爬取
    1. 直接爬取
    2. 按照日期爬取
  
2. 导出词云图

3. 导出Excel文件

## 实现方式
| 目标  | 工具  |
|:-----|:------:|
| GUI  | Pyqt5|
| .ui-->.py | QtDesigner  |

## 更新
**Before**<br/>
爬取历史弹幕的api地址为https://api.bilibili.com/x/v2/dm/web/history?type=1&oid={oid}&date={date}
返回xml文件

**After**<br/>
爬取历史弹幕的api地址为https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={oid}&date={date}
返回seg.so弹幕文件,为protobuf格式
要解析protobuf格式的文件，需要安装protoc编译器（配置环境变量）、protobuf-python，编写proto结构文件。
利用protoc命令指定输出路径和输入文件
执行完成后会生成xx_pb2.py文件
```python
from xx_pb2 import DmSegMobileReply
from google.protobuf.json_format import MessageToJson, Parse

dm = DmSegMobileReply()
dm.ParseFromString(res.content)  #二进制编码格式
data_dict = json.loads(MessageToJson(dm))  #json.loads将json转换成dict
```
参考文章：https://blog.csdn.net/freeking101/article/details/123131304

## 进一步优化
- 爬取日志
- 创建任务列表，用户可从一系列爬取任务中选择是否导出为词云图或Excel文件

