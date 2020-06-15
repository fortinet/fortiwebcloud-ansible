#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import copy
import requests
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.fortiwebcloud import CloudWafAPIHandler
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.waf_config import update_waf_config

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'Fortinet'
}

FAIL_SOCKET_MSG = {"msg": "Socket Path Empty! The persistent connection manager is messed up. "
                   "Try again in a few moments."}

DOCUMENTATION = '''
---
module: cloud_waf_ip_protection_method
author: "Fortinet"
version_added: "2.9"
short_description: "Execute the Restful API to configure IP address protection."
description:
    - "This module will configure the IP address protection to an application or a template on Fortiweb Cloud by the Restful API
   . Before using this module, you must be a Fortinet inc. customer."
requirements:
    - requests
options:
    app_name:
        description:
            - The application name you want to configure.
        required: False
        type: str
    temp_name:
        description:
            - The template name you want to configure.
        required: False
        type: str
    status:
        description:
            - Enable/disable IP address protection.
        required: True
        type: str
        choices:
            - enable
            - disable
    template_status:
        description:
            - Enable/disable the module's template status.
        required: False
        type: str
        default: disable
        choices:
            - enable
            - disable
    IPProtection:
        description:
            - Configure IP address protection.
        required: True
        type: dict
        suboptions:
            ip-reputation:
                description:
                    - Configure the ability to allow (enable) or deny (disable) requests from clients based upon their current reputation as known to FortiWeb Cloud.
                type: str
                choices:
                    - enable
                    - disable
            geo-ip-block:
                description:
                    - List of countries from which client requests are blocked. For example: American Samoa, Denmark, Iran.
                type: dict
                suboptions:
                    members:
                        description:
                            - The country's name list.
                        type: list
                        choices:
                            - Afghanistan
                            - Aland Islands
                            - Albania
                            - Algeria
                            - American Samoa
                            - Andorra
                            - Angola
                            - Anguilla
                            - Antarctica
                            - Antigua And Barbuda
                            - Argentina
                            - Armenia
                            - Aruba
                            - Australia
                            - Austria
                            - Azerbaijan
                            - Bahamas
                            - Bahrain
                            - Bangladesh
                            - Barbados
                            - Belarus
                            - Belgium
                            - Belize
                            - Benin
                            - Bermuda
                            - Bhutan
                            - Bolivia
                            - Bonaire Saint Eustatius And Saba
                            - Bosnia And Herzegovina
                            - Botswana
                            - Brazil
                            - British Indian Ocean Territory
                            - British Virgin Islands
                            - Brunei Darussalam
                            - Bulgaria
                            - Burkina Faso
                            - Burundi
                            - Cambodia
                            - Cameroon
                            - Canada
                            - Cape Verde
                            - Cayman Islands
                            - Central African Republic
                            - Chad
                            - Chile
                            - China
                            - Colombia
                            - Comoros
                            - Congo
                            - Cook Islands
                            - Costa Rica
                            - Cote D'Ivoire
                            - Croatia
                            - Cuba
                            - Curacao
                            - Cyprus
                            - Czech Republic
                            - Democratic People'S Republic Of Korea
                            - Democratic Republic Of The Congo
                            - Denmark
                            - Djibouti
                            - Dominica
                            - Dominican Republic
                            - Ecuador
                            - Egypt
                            - El Salvador
                            - Equatorial Guinea
                            - Eritrea
                            - Estonia
                            - Ethiopia
                            - Falkland Islands (Malvinas)
                            - Faroe Islands
                            - Federated States Of Micronesia
                            - Fiji
                            - Finland
                            - France
                            - French Guiana
                            - French Polynesia
                            - Gabon
                            - Gambia
                            - Georgia
                            - Germany
                            - Ghana
                            - Gibraltar
                            - Greece
                            - Greenland
                            - Grenada
                            - Guadeloupe
                            - Guam
                            - Guatemala
                            - Guernsey
                            - Guinea
                            - Guinea-Bissau
                            - Guyana
                            - Haiti
                            - Honduras
                            - Hong Kong
                            - Hungary
                            - Iceland
                            - India
                            - Indonesia
                            - Iran
                            - Iraq
                            - Ireland
                            - Isle Of Man
                            - Israel
                            - Italy
                            - Jamaica
                            - Japan
                            - Jersey
                            - Jordan
                            - Kazakhstan
                            - Kenya
                            - Kiribati
                            - Kosovo
                            - Kuwait
                            - Kyrgyzstan
                            - Lao People'S Democratic Republic
                            - Latvia
                            - Lebanon
                            - Lesotho
                            - Liberia
                            - Libya
                            - Liechtenstein
                            - Lithuania
                            - Luxembourg
                            - Macao
                            - Macedonia
                            - Madagascar
                            - Malawi
                            - Malaysia
                            - Maldives
                            - Mali
                            - Malta
                            - Marshall Islands
                            - Martinique
                            - Mauritania
                            - Mauritius
                            - Mayotte
                            - Mexico
                            - Moldova
                            - Monaco
                            - Mongolia
                            - Montenegro
                            - Montserrat
                            - Morocco
                            - Mozambique
                            - Myanmar
                            - Namibia
                            - Nauru
                            - Nepal
                            - Netherlands
                            - New Caledonia
                            - New Zealand
                            - Nicaragua
                            - Niger
                            - Nigeria
                            - Niue
                            - Norfolk Island
                            - Northern Mariana Islands
                            - Norway
                            - Oman
                            - Pakistan
                            - Palau
                            - Palestine
                            - Panama
                            - Papua New Guinea
                            - Paraguay
                            - Peru
                            - Philippines
                            - Poland
                            - Portugal
                            - Puerto Rico
                            - Qatar
                            - Republic Of Korea
                            - Reunion
                            - Romania
                            - Russian Federation
                            - Rwanda
                            - Saint Bartelemey
                            - Saint Kitts And Nevis
                            - Saint Lucia
                            - Saint Martin
                            - Saint Pierre And Miquelon
                            - Saint Vincent And The Grenadines
                            - Samoa
                            - San Marino
                            - Sao Tome And Principe
                            - Saudi Arabia
                            - Senegal
                            - Serbia
                            - Seychelles
                            - Sierra Leone
                            - Singapore
                            - Sint Maarten
                            - Slovakia
                            - Slovenia
                            - Solomon Islands
                            - Somalia
                            - South Africa
                            - South Georgia And The South Sandwich Islands
                            - South Sudan
                            - Spain
                            - Sri Lanka
                            - Sudan
                            - Suriname
                            - Swaziland
                            - Sweden
                            - Switzerland
                            - Syria
                            - Taiwan
                            - Tajikistan
                            - Tanzania
                            - Thailand
                            - Timor-Leste
                            - Togo
                            - Tokelau
                            - Tonga
                            - Trinidad And Tobago
                            - Tunisia
                            - Turkey
                            - Turkmenistan
                            - Turks And Caicos Islands
                            - Tuvalu
                            - U.S. Virgin Islands
                            - Uganda
                            - Ukraine
                            - United Arab Emirates
                            - United Kingdom
                            - United States
                            - Uruguay
                            - Uzbekistan
                            - Vanuatu
                            - Vatican
                            - Venezuela
                            - Vietnam
                            - Wallis And Futuna
                            - Yemen
                            - Zambia
                            - Zimbabwe
            ip-list:
                description:
                  - Configure the trust IP address list, block IP address list or allow-only-ip list.
                type: dict
                suboptions:
                    members:
                        description:
                            - The ip list.
                        type: list
                        elements: dict
                        suboptions:
                            type:
                                description:
                                    - The type of IP address list.
                                type: str
                                choices:
                                    - trust-ip
                                    - block-ip
                                    - allow-only-ip
                            ip:
                                description:
                                    - The client’s source IP address. It can be a single IP address or a range of addresses.
                                    (e.g., 172.22.14.1-172.22.14.256)
                                type: str
'''
EXAMPLES = '''
---
- hosts: fortiwebcloud01
  name: Execute cloud api
  collections:
   - fortinet.fortiwebcloud
  gather_facts: no
  connection: httpapi
  vars:
    ansible_httpapi_validate_certs: False
    ansible_httpapi_use_ssl: True
    ansible_httpapi_port: 443
    application_name:  "YOUR_APP_NAME"
  tasks:
  - name: Configure IP address Protection.
    cloud_waf_ip_protection_method:
      app_name: "{{application_name}}"
      template_status: disable
      status: enable
      IPProtection:
        ip-reputation: enable
        geo-ip-block:
          members:
            - Antigua And Barbuda
            - Aland Islands
            - Afghanistan
        ip-list:
          members:
            - type: trust-ip
              ip: '1.1.1.1,2.2.2.21-2.2.2.27'
            - type: block-ip
              ip: '3.1.1.1,3.1.1.11-3.1.1.17'
            - type: allow-only-ip
              ip: '4.1.1.1-4.1.1.17,4.1.1.19'
'''

RETURN = '''
alias:
    description: The new alias name for your domain, you should change your domain's server address to this address in the DNS.
    returned: always
    type: str
    sample: demo.example.com
msg:
    description: Returns the result of the app configuration.
    returned: always
    type: str
'''

def main():
    fields = {
        "api_token": {"required": False, "type": "str", "default": ""},
        "app_name": {"required": False, "type": "str"},
        "temp_name": {"required": False, "type": "str"},
        "status": {"required": True, "type": "str", "choices": ["enable", "disable"]},
        "template_status": {"required": False, "type": "str", "choices": ["enable", "disable"]},
        "IPProtection": {
            "required": True, "type": "dict",
            "options": {
                "ip-reputation": {"type": "str", "choices": ["enable", "disable"]},
                "geo-ip-block": {
                    "type": "dict", "default": None,
                    "options": {
                        "members": {
                            "type": "list",
                            "choices": ["Afghanistan","Aland Islands","Albania","Algeria","American Samoa","Andorra",
                                        "Angola","Anguilla","Antarctica","Antigua And Barbuda","Argentina","Armenia",
                                        "Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh",
                                        "Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia",
                                        "Bonaire Saint Eustatius And Saba","Bosnia And Herzegovina","Botswana","Brazil",
                                        "British Indian Ocean Territory","British Virgin Islands","Brunei Darussalam",
                                        "Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde",
                                        "Cayman Islands","Central African Republic","Chad","Chile","China","Colombia",
                                        "Comoros","Congo","Cook Islands","Costa Rica","Cote D'Ivoire","Croatia","Cuba",
                                        "Curacao","Cyprus","Czech Republic","Democratic People'S Republic Of Korea",
                                        "Democratic Republic Of The Congo","Denmark","Djibouti","Dominica",
                                        "Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea",
                                        "Eritrea","Estonia","Ethiopia","Falkland Islands (Malvinas)","Faroe Islands",
                                        "Federated States Of Micronesia","Fiji","Finland","France","French Guiana",
                                        "French Polynesia","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar",
                                        "Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guernsey",
                                        "Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary",
                                        "Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle Of Man","Israel",
                                        "Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya","Kiribati",
                                        "Kosovo","Kuwait","Kyrgyzstan","Lao People'S Democratic Republic","Latvia",
                                        "Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg",
                                        "Macao","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta",
                                        "Marshall Islands","Martinique","Mauritania","Mauritius","Mayotte","Mexico",
                                        "Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique",
                                        "Myanmar","Namibia","Nauru","Nepal","Netherlands","New Caledonia","New Zealand",
                                        "Nicaragua","Niger","Nigeria","Niue","Norfolk Island","Northern Mariana Islands",
                                        "Norway","Oman","Pakistan","Palau","Palestine","Panama","Papua New Guinea",
                                        "Paraguay","Peru","Philippines","Poland","Portugal","Puerto Rico","Qatar",
                                        "Republic Of Korea","Reunion","Romania","Russian Federation","Rwanda",
                                        "Saint Bartelemey","Saint Kitts And Nevis","Saint Lucia","Saint Martin",
                                        "Saint Pierre And Miquelon","Saint Vincent And The Grenadines","Samoa",
                                        "San Marino","Sao Tome And Principe","Saudi Arabia","Senegal","Serbia",
                                        "Seychelles","Sierra Leone","Singapore","Sint Maarten","Slovakia","Slovenia",
                                        "Solomon Islands","Somalia","South Africa",
                                        "South Georgia And The South Sandwich Islands","South Sudan","Spain",
                                        "Sri Lanka","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria",
                                        "Taiwan","Tajikistan","Tanzania","Thailand","Timor-Leste","Togo","Tokelau",
                                        "Tonga","Trinidad And Tobago","Tunisia","Turkey","Turkmenistan",
                                        "Turks And Caicos Islands","Tuvalu","U.S. Virgin Islands","Uganda","Ukraine",
                                        "United Arab Emirates","United Kingdom","United States","Uruguay","Uzbekistan",
                                        "Vanuatu","Vatican","Venezuela","Vietnam","Wallis And Futuna","Yemen","Zambia",
                                        "Zimbabwe"]
                        }
                    }
                },
                "ip-list": {
                    "type": "dict",
                    "options": {
                        "members": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "type": {
                                    "type": "str",
                                    "choices": ["trust-ip", "block-ip", "allow-only-ip"]
                                },
                                "ip": {
                                    "type": "str"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    module = AnsibleModule(
        argument_spec=fields,
        supports_check_mode=True
    )
    result = dict(
        changed=False,
        msg='The module was successfully executed.'
    )
    if module.check_mode:
        module.exit_json(**result)

    if module.params.get('app_name') and module.params.get('temp_name'):
        module.fail_json(msg="Please input the application name or template name.")

    if not((module.params.get('app_name') or module.params.get('temp_name'))
            and module.params.get('IPProtection') and module.params.get('status')):
        module.fail_json(msg="Required parameters must not be empty.")

    if module._socket_path:
        connection = Connection(module._socket_path)
        api_handler = CloudWafAPIHandler(connection, token=module.params.get("api_token"))

        data = copy.deepcopy(module.params)
        data['_status'] = data.pop('status')

        try:
            is_error, changed, res = update_waf_config(data, api_handler, 'IPProtection')
            if not is_error:
                result["meta"] = res
                result["changed"] = changed
                module.exit_json(**result)
            else:
                result["meta"] = res
                result["msg"] = "Error in repo"
                module.fail_json(**result)

        except Exception as e:
            module.fail_json(msg="During app configuration, an error occurred:" + str(e))
    else:
        module.fail_json(
            msg="Socket Path Empty! A persistent connection manager error occurred. Try again in a few moments.")




if __name__ == '__main__':
    main()
