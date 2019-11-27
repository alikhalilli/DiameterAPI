SCAPDef = {
    'Command-Code': {
        'code': '999',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'Auth-Application-Id': {
        'code': '258',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'Re-Auth-Request-Type': {
        'code': '285',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'AUTHORIZE_ONLY': '0'
        }, {
            'AUTHORIZE_AUTHENTICATE': '1'
        }]
    },
    'Redirect-Max-Cache-Time': {
        'code': '262',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'Destination-Host': {
        'code': '293',
        'type': 'DiameterIdentity',
        'mandatory': 1
    },
    'Destination-Realm': {
        'code': '283',
        'type': 'DiameterIdentity',
        'mandatory': 1
    },
    'Event-Timestamp': {
        'code': '55',
        'type': 'Time',
        'mandatory': 1
    },
    'Failed-AVP': {
        'code': '279',
        'type': 'Grouped',
        'mandatory': 1
    },
    'Origin-Host': {
        'code': '264',
        'type': 'DiameterIdentity',
        'mandatory': 1
    },
    'Error-Message': {
        'code': '281',
        'type': 'UTF8String',
        'mandatory': 1
    },
    'Error-Reporting-Host': {
        'code': '294',
        'type': 'DiameterIdentity',
        'mandatory': 1
    },
    'Origin-Realm': {
        'code': '296',
        'type': 'DiameterIdentity',
        'mandatory': 1
    },
    'Origin-State-Id': {
        'code': '278',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'Proxy-Info': {
        'code': '284',
        'type': 'Grouped',
        'mandatory': 1
    },
    'Proxy-Host': {
        'code': '280',
        'type': 'DiameterIdentity',
        'mandatory': 1
    },
    'Proxy-State': {
        'code': '33',
        'type': 'OctetString',
        'mandatory': 1
    },
    'Redirect-Host': {
        'code': '292',
        'type': 'DiameterURI',
        'mandatory': 1
    },
    'Redirect-Host-Usage': {
        'code': '261',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'DONT_CACHE': '0'
        }, {
            'ALL_SESSION': '1'
        }, {
            'ALL_REALM': '2'
        }, {
            'REALM_AND_APPLICATION': '3'
        }, {
            'ALL_APPLICATION': '4'
        }, {
            'ALL_HOST': '5'
        }, {
            'ALL_USER': '6'
        }]
    },
    'Result-Code': {
        'code': '268',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'Route-Record': {
        'code': '282',
        'type': 'DiameterIdentity',
        'mandatory': 1
    },
    'Session-Id': {
        'code': '263',
        'type': 'UTF8String',
        'mandatory': 1
    },
    'Termination-Cause': {
        'code': '295',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'DIAMETER_LOGOUT': '1'
        }, {
            'DIAMETER_SERVICE_NOT_PROVIDED': '2'
        }, {
            'DIAMETER_BAD_ANSWER': '3'
        }, {
            'DIAMETER_ADMINISTRATIVE': '4'
        }, {
            'DIAMETER_LINK_BROKEN': '5'
        }, {
            'DIAMETER_AUTH_EXPIRED': '6'
        }, {
            'DIAMETER_USER_MOVED': '7'
        }, {
            'DIAMETER_SESSION_TIMEOUT': '8'
        }]
    },
    'User-Name': {
        'code': '1',
        'type': 'UTF8String',
        'mandatory': 1
    },
    'CC-Request-Number': {
        'code': '415',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'CC-Request-Type': {
        'code': '416',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'INITIAL_REQUEST': '1'
        }, {
            'UPDATE_REQUEST': '2'
        }, {
            'TERMINATION_REQUEST': '3'
        }, {
            'EVENT_REQUEST': '4'
        }]
    },
    'CC-Session-Failover': {
        'code': '418',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'FAILOVER_NOT_SUPPORTED': '0'
        }, {
            'FAILOVER_SUPPORTED': '1'
        }]
    },
    'Credit-Control-Failure-Handling': {
        'code': '427',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'TERMINATE': '0'
        }, {
            'CONTINUE': '1'
        }, {
            'RETRY_AND_TERMINATE': '2'
        }]
    },
    'Multiple-Services-Credit-Control': {
        'code': '456',
        'type': 'Grouped',
        'mandatory': 1
    },
    'Multiple-Services-Indicator': {
        'code': '455',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'MULTIPLE_SERVICES_NOT_SUPPORTED': '0'
        }, {
            'MULTIPLE_SERVICES_SUPPORTED': '1'
        }]
    },
    'Requested-Service-Unit': {
        'code': '437',
        'type': 'Grouped',
        'mandatory': 1
    },
    'Service-Context-Id': {
        'code': '461',
        'type': 'UTF8String',
        'mandatory': 1
    },
    'Subscription-Id': {
        'code': '443',
        'type': 'Grouped',
        'mandatory': 1
    },
    'User-Equipment-Info': {
        'code': '458',
        'type': 'Grouped',
        'mandatory': 1
    },
    'Service-Identifier': {
        'code': '439',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'CC-Input-Octets': {
        'code': '412',
        'type': 'Unsigned64',
        'mandatory': 1
    },
    'CC-Output-Octets': {
        'code': '414',
        'type': 'Unsigned64',
        'mandatory': 1
    },
    'CC-Service-Specific-Units': {
        'code': '417',
        'type': 'Unsigned64',
        'mandatory': 1
    },
    'CC-Time': {
        'code': '420',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'CC-Total-Octets': {
        'code': '421',
        'type': 'Unsigned64',
        'mandatory': 1
    },
    'Final-Unit-Indication': {
        'code': '430',
        'type': 'Grouped',
        'mandatory': 1
    },
    'Granted-Service-Unit': {
        'code': '431',
        'type': 'Grouped',
        'mandatory': 1
    },
    'Rating-Group': {
        'code': '432',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'Redirect-Address-Type': {
        'code': '433',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'IPv4_Address': '0'
        }, {
            'IPv6_Address': '1'
        }, {
            'URL': '2'
        }, {
            'SIP_URI': '3'
        }]
    },
    'Redirect-Server': {
        'code': '434',
        'type': 'Grouped',
        'mandatory': 1
    },
    'Redirect-Server-Address': {
        'code': '435',
        'type': 'UTF8String',
        'mandatory': 1
    },
    'Subscription-Id-Data': {
        'code': '444',
        'type': 'UTF8String',
        'mandatory': 1
    },
    'Used-Service-Unit': {
        'code': '446',
        'type': 'Grouped',
        'mandatory': 1
    },
    'Validity-Time': {
        'code': '448',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'Final-Unit-Action': {
        'code': '449',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'TERMINATE': '0'
        }, {
            'REDIRECT': '1'
        }]
    },
    'Subscription-Id-Type': {
        'code': '450',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'END_USER_E164': '0'
        }, {
            'END_USER_IMSI': '1'
        }, {
            'END_USER_SIP_URI': '2'
        }, {
            'END_USER_NAI': '3'
        }, {
            'END_USER_PRIVATE': '4'
        }]
    },
    'Tariff-Time-Change': {
        'code': '451',
        'type': 'Time',
        'mandatory': 1
    },
    'Tariff-Change-Usage': {
        'code': '452',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'UNIT_BEFORE_TARIFF_CHANGE': '0'
        }, {
            'UNIT_AFTER_TARIFF_CHANGE': '1'
        }, {
            'UNIT_INDETERMINATE': '2'
        }]
    },
    'User-Equipment-Info-Type': {
        'code': '459',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'IMEISV': '0'
        }, {
            'MAC': '1'
        }, {
            'EUI64': '2'
        }, {
            'MODIFIED_EUI64': '3'
        }]
    },
    'User-Equipment-Info-Value': {
        'code': '460',
        'type': 'OctetString',
        'mandatory': 1
    },
    '3GPP-MS-TimeZone': {
        'code': '23',
        'type': 'OctetString',
        'mandatory': 1
    },
    'Time-Quota-Threshold': {
        'code': '868',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'Volume-Quota-Threshold': {
        'code': '869',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'Unit-Quota-Threshold': {
        'code': '1226',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'Account-Location': {
        'code': '1073',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'Subscription-Id-Location': {
        'code': '1074',
        'type': 'UTF8String',
        'mandatory': 1
    },
    'Other-Party-Id': {
        'code': '1075',
        'type': 'Grouped',
        'mandatory': 1
    },
    'Other-Party-Id-Nature': {
        'code': '1076',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'UNKNOWN': '0'
        }, {
            'INTERNATIONAL': '1'
        }, {
            'NATIONAL': '2'
        }]
    },
    'Other-Party-Id-Data': {
        'code': '1077',
        'type': 'UTF8String',
        'mandatory': 1
    },
    'Other-Party-Id-Type': {
        'code': '1078',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'END_USER_E164': '0'
        }, {
            'END_USER_IMSI': '1'
        }, {
            'END_USER_SIP_URI': '2'
        }, {
            'END_USER_NAI': '3'
        }]
    },
    'Service-Provider-Id': {
        'code': '1081',
        'type': 'UTF8String',
        'mandatory': 1
    },
    'Traffic-Case': {
        'code': '1082',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'Service-Parameter-Info': {
        'code': '440',
        'type': 'Grouped',
        'mandatory': 1
    },
    'Service-Parameter-Type': {
        'code': '441',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'Service-Parameter-Value': {
        'code': '442',
        'type': 'OctetString',
        'mandatory': 1
    },
    'Cost-Information': {
        'code': '423',
        'type': 'Grouped',
        'mandatory': 1
    },
    'Unit-Value': {
        'code': '445',
        'type': 'Grouped',
        'mandatory': 1
    },
    'Value-Digits': {
        'code': '447',
        'type': 'Integer64',
        'mandatory': 1
    },
    'Exponent': {
        'code': '429',
        'type': 'Integer32',
        'mandatory': 1
    },
    'Currency-Code': {
        'code': '425',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'Cost-Unit': {
        'code': '424',
        'type': 'UTF8String',
        'mandatory': 1
    },
    'Result-Code-Extension': {
        'code': '1067',
        'type': 'Unsigned32',
        'mandatory': 1
    },
    'CC-Money': {
        'code': '413',
        'type': 'Grouped',
        'mandatory': 1
    },
    'Requested-Action': {
        'code': '436',
        'type': 'Enumerated',
        'mandatory': 1,
        'enumInfo': [{
            'DIRECT_DEBITING': '0'
        }, {
            'REFUND_ACCOUNT': '1'
        }, {
            'CHECK_BALANCE': '2'
        }, {
            'PRICE_ENQUIRY': '3'
        }]
    },
    'CC-Correlation-Id': {
        'code': '411',
        'type': 'OctetString',
        'mandatory': 1
    },
    'Acct-Multi-Session-Id': {
        'code': '50',
        'type': 'UTF8String',
        'mandatory': 1
    }
}
