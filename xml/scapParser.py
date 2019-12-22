import xml.dom.minidom as minidom

xml_dictionary = minidom.parse(
    '/Users/aliganbarkhalilli/git_repos/DiameterAPI/scap.xml').documentElement


avpWithName = {}
avpWithCode = {}

for node in xml_dictionary.getElementsByTagName('AVP_Def'):
    avpWithName[node.getAttribute('name')] = dict(
        code=node.getAttribute('code'),
        type=node.getAttribute('type'),
        mandatory=1 if node.getAttribute('mandatoryFlag') else 0
    )

    if node.getAttribute('type') == 'Enumerated':
        enumList = []
        for enum in node.getElementsByTagName('EnumValue'):
            enumList.append({enum.getAttribute('comment')
                            : enum.getAttribute('value')})
        avpWithName[node.getAttribute('name')].update({'enumInfo': enumList})

    avpWithCode[node.getAttribute('code')] = dict(
        name=node.getAttribute('name'),
        type=node.getAttribute('type'),
        mandatory=1 if node.getAttribute('mandatoryFlag') else 0
    )

print(avpWithName)
# print(avpWithCode)
