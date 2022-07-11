import struct
import datetime

# 格式
# 0xAA08
# BinHead:8 version 1 maxStockCnt 8000 stockId(length)
# StockLabelId * maxStockCnt
# DataPos      * maxStockCnt
# 变长数据，通过 DataPos offset size 来定位

def reviseStr(bstr):
    return bstr.rstrip(b'\x00').decode('gbk')

def dumpMarket(data):
    # magic
    (magic, version, maxStockCnt, stockLen) = struct.unpack('<HHHH', data[:8])
    print(magic, version, maxStockCnt, stockLen)
    assert(magic == 0xAA09)
    assert(version == 1)
    print(maxStockCnt, stockLen)
    offset = 8

    labelIdSz = 16
    dataPosSz = 8
    marketSz = 84
    stockSz = 48

    labelIdBuf = data[offset: offset + labelIdSz * maxStockCnt]
    offset += labelIdSz * maxStockCnt

    dataPosBuf = data[offset: offset + dataPosSz * maxStockCnt]
    offset += dataPosSz * maxStockCnt

    for idx in range(stockLen):
        label, idx  = struct.unpack('<12sI', labelIdBuf[idx * labelIdSz: (idx + 1) * labelIdSz])
        label = label.rstrip(b'\x00').decode()
        itemOffset, itemSz = struct.unpack('<II', dataPosBuf[idx * dataPosSz: (idx + 1) * dataPosSz])

        print(label, idx, itemOffset, itemSz)
        item = data[offset + itemOffset: offset + itemOffset + itemSz]
        (
            marketId,  # 市场代码, 'HS', 'SZ', 'JZ', 'HW' .....
            marketName,  # 市场名称(英文简称，如 SHSE 表示上海交易所)
            localTime,  # 时区
            marketKind,  # 市场属性(1 股票；3 期货)
            _,
            periodCount,  # 交易时段个数
            # 开市时间 1,2,3,4,5 (开盘分钟数，比如 0X023A（570）表示 9:30)
            open0, open1, open2, open3, open4, open5, open6, open7,
            # 收市时间 1,2,3,4,5
            close0, close1, close2, close3, close4, close5, close6, close7,
            _,
            # 该市场的证券个数
            count
        ) = struct.unpack('<2s32siHHh'+('h'*8)+('h'*8)+'II', item[:marketSz])
        marketId = reviseStr(marketId)
        marketName = reviseStr(marketName)
        print(marketId, marketName)
        for stkIdx in range((len(item)-marketSz) // stockSz):
            stkData = item[marketSz + stkIdx * stockSz : marketSz + (stkIdx + 1) * stockSz]
            (
                _,
                stockId,  # 股票代码,以'\0'结尾
                stockName,  # 股票名称,以'\0'结尾
                block,  # 品种属性，0指数，1 A、B股，2 基金, 3 债券，4 质押 ，7 期货，8 期货指数
                pointCount,  # 小数点个数0X00、0X01、0X02、0X03
                hand
            ) = struct.unpack('<H10s32scch', stkData)
            stockId = reviseStr(stockId)
            stockName = reviseStr(stockName)
            print(marketId+stockId, stockName)

