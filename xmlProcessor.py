import xml.dom.minidom as minidom


xml_dictionary = minidom.parse(
    '/Users/akhalilli/gitrepos/diamAPI/dictionary.xml').documentElement
dict_avps = xml_dictionary.getElementsByTagName("avp")
dict_vendors = xml_dictionary.getElementsByTagName("vendor")
dict_commands = xml_dictionary.getElementsByTagName("command")


avpDict = {}
for avpItem in dict_avps:
    avpDict[avpItem.getAttribute('name')] = dict(
        code=avpItem.getAttribute('code'),
        mandatory=avpItem.getAttribute('mandatory'),
        mayencrypt=avpItem.getAttribute('may-encrypt'),
        protected=avpItem.getAttribute('protected'),
        vendorbit=avpItem.getAttribute('vendor-bit'),
        vendorid=avpItem.getAttribute('vendor-id')
    )
    for typedef in avpItem.getElementsByTagName('type'):
        avpDict[avpItem.getAttribute('name')].update(
            dict(typename=typedef.getAttribute('type-name')))
        if typedef.getAttribute('type-name') == 'Enumerated':
            avpDict[avpItem.getAttribute('name')]['enumList'] = []
            enumInfo = {}
            for enumItem in avpItem.getElementsByTagName('enum'):
                enumInfo = {'name': enumItem.getAttribute('name'),
                            'code': enumItem.getAttribute('code')}
                avpDict[avpItem.getAttribute(
                    'name')]['enumList'].append(enumInfo)
# print(avpDict)
