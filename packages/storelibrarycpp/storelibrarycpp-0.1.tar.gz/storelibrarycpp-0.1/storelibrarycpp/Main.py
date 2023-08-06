def getStockStatus(stockCount):
    if(stockCount == 0):
        return "OUT OF STOCK"
    elif(stockCount < 50):
        return "LOW STOCK"
    else:
        return "IN STOCK"
