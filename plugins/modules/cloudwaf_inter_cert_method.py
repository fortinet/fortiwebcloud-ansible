#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import copy
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.fortiwebcloud import CloudWafAPIHandler
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.waf_config import update_waf_config, \
    get_waf_config

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'Fortinet'
}


DOCUMENTATION = '''
---
module: cloud_waf_inter_cert_method
author: "Fortinet"
version_added: "2.9"
short_description: "Execute the Restful API to configure or delete intermediate certificates."
description:
    - "This module will configure or delete intermediate certificates to an application on Fortiweb Cloud by the Restful API.
    Before using this module, you must be a Fortinet inc. customer."
requirements:
    - requests
options:
    app_name:
        description:
            - The name of the application you want to configure.
        required: True
        type: str
    action:
        description:
            - The type of update operation.
        required: True
        type: str
        choices:
            - import
            - delete
            - get
    certificate:
        description:
            - The intermediate certificate to be imported; required for an action of 'import'.
        required: False
        type: str
    id:
        description:
            - The id of the certificate to be deleted; required for an action of 'delete'.
        required: False
        type: int
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
  - name: Configure intermediate certificates.
    cloud_waf_inter_cert_method:
      app_name: "{{application_name}}"
      action: import
      certificate: |
        <YOUR-CERTIFICATE>
'''

RETURN = '''
alias:
    description: The ID of the imported certificate.
    returned: always
    type: str
    sample: <123>
msg:
    description: Returns the result of the app configuration.
    returned: always
    type: str
'''


def main():
    fields = {
        "api_token": {"required": False, "type": "str", "default": ""},
        "app_name": {"required": True, "type": "str"},
        "action": {"required": True, "type": "str", "choices": ["import", "delete", "get"]},
        "certificate": {"required": False, "type": "str"},
        "id": {"required": False, "type": "int"}
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

    if ((module.params.get('action') == 'import' and not module.params.get('certificate')) or
       (module.params.get('action') == 'delete' and not module.params.get('id'))):
        module.fail_json(msg="Required parameters must not be empty.")

    if module.params.get('action') == 'import':
        module.params.pop('id')
    elif module.params.get('action') == 'delete':
        module.params.pop('certificate')
    else:
        module.params.pop('id')
        module.params.pop('certificate')

    if module._socket_path:
        connection = Connection(module._socket_path)
        api_handler = CloudWafAPIHandler(connection, token=module.params.get("api_token"))
        data = copy.deepcopy(module.params)
        if module.params.get('action') == 'get':
            con = dict({"size": 10, "cursor": "", "forward": True})
            is_error, changed, res = get_waf_config(data, api_handler, 'intercertificate', con)
            con['cursor'] = res['next_cursor']
            hits=res['hits']
            while res['next_cursor']:
                is_error, changed, res = get_waf_config(data, api_handler, 'intercertificate', con)
                con['cursor'] = res['next_cursor']
                hits = hits + res['hits']

            result["meta"] = hits
            result["changed"] = changed
            module.exit_json(**result)
        else:
            try:
                is_error, changed, res = update_waf_config(data, api_handler, 'intercertificate')
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
