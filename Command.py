from static import commandDict, vendorDict


class Command:
    @staticmethod
    def getCodeByName(name):
        return commandDict[name]['code']

    @staticmethod
    def getVendorIDByName(name):
        return commandDict[name]['vendor-id']

    @staticmethod
    def getNameByCode(code):
        for k, v in commandDict.items():
            if v['code'] == code:
                return k

    @staticmethod
    def getVendorIDByCode(code):
        for _, v in vendorDict.items():
            if v['code'] == code:
                return v['vendor-id']
