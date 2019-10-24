from static import vendorDict


class Vendor:
    @staticmethod
    def getCodeById(id):
        return vendorDict[id]['code']

    @staticmethod
    def getNameById(id):
        return vendorDict[id]['code']

    @staticmethod
    def getNameByCode(code):
        for _, v in vendorDict.items():
            if v['code'] == code:
                return v['name']

    @staticmethod
    def getIdByCode(code):
        for k, v in vendorDict.items():
            if v['code'] == code:
                return k
