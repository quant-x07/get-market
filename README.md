# get-market
获取市场信息（市场类型、交易时段等），以及股票列表（代码、名称、精度、手等）

## 如何运行
* 安装 python3（在python3.8 linux、windows环境验证通过）

* 准备 requests 依赖包
```
pip3 install requests
```

* 运行
```
cd get-xrxd-py
python3 main.py
```

* 输出
```
43529 1 100 2
100 2
SH 0 0 918900
SH SHSE
SH000001 上证指数
SH000002 Ａ股指数
SH000003 Ｂ股指数
SH000004 工业指数
```

注意 默认体验密码和服务器地址都已经在程序中固定，有需求可以联系我们获取独立的用户名密码
