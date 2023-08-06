### function_tool工具包

安装：
```shell
pip install function_tool
```

本工具包对一些常用的功能进行了Python封装，目前主要包含以下功能：

### 1. 日期时间类
DateTimeTool
+ timestamp2time函数：Unix时间戳转时间字符串
+ time2timestamp函数：时间字符串转Unix时间戳
+ get_range_of_date_by_str函数：返回给定时间所在日期的时间戳范围
使用示例
```python
from function_tool_derrick.UsualTool import DateTimeTool    # 导入function_tool_derrick.UsualTool下的DateTimeTool类

if __name__ == '__main__':
    print(DateTimeTool.timestamp2time(1681721029)) # 打印 2023-04-17 16:43:49
    print(DateTimeTool.time2timestamp('2023-04-17 16:43:49')) # 打印 1681721029

    ret = DateTimeTool.get_range_of_date_by_str('2022-02-02 15:30:28', formatter='%Y-%m-%d %H:%M:%S', tsType=TimestampType.MILLISECOND)
    print(ret) # 打印 [1643731200000, 1643817599999]
```