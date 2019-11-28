from static import avpDict, vendorDict, commandDict


class AVPTools:
    """
    'code': '60',
    'mandatory': 'must',
    'mayencrypt': 'yes',
    'protected': 'may',
    'vendorbit': 'mustnot',
    'vendorid': '',
    'typename': 'OctetString'
    """
    @staticmethod
    def getAllDetailsByName(name):
        return avpDict[name]

    @staticmethod
    def getCodeByName(name):
        try:
            return avpDict[name]['code']
        except KeyError:
            print('AVP Not Found')

    @staticmethod
    def getNameByCode(code):
        for k, v in avpDict.items():
            if v['code'] == code:
                return k

    @staticmethod
    def getTypeByCode(code):
        for _, v in avpDict.items():
            if v['code'] == str(code):
                return v['typename']

    @staticmethod
    def getMandatoryByName(name):
        return avpDict[name]['mandatory']

    @staticmethod
    def getMayEncryptByName(name):
        return avpDict[name]['mayencrypt']

    @staticmethod
    def getProtectedByName(name):
        return avpDict[name]['protected']

    @staticmethod
    def getVendorBitByName(name):
        return avpDict[name]['vendorbit']

    @staticmethod
    def getVendorIdByName(name):
        return '0' if avpDict[name]['vendorid'] == "" else avpDict[name]['vendorid']

    @staticmethod
    def getTypeByName(name):
        try:
            return avpDict[name]['typename']
        except KeyError:
            print("AVP Not Found")

    @staticmethod
    def isEnum(name):
        return AVPTools.getTypeByName == 'Enumerated'
