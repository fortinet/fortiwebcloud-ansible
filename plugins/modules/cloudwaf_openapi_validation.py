#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.fortiwebcloud import CloudWafAPIHandler
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.openapivalidation import setup_openapi_validation

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'Fortinet'
}

DOCUMENTATION = '''
---
module: cloudwaf_openapi_validation
author: "Fortinet"
version_added: "2.9"
short_description: "Execute the Restful API to setup OpenAPI Validation."
description:
    - "This module will setup OpenAPI Validation for an application on Fortiweb Cloud by the Restful API.
    Before using this module, you must be a Fortinet inc. customer."

options:
    app_name:
        description:
            - Any name you want for your app.
        required: True
    force:
        description:
            - Force set the openapi validation. 
            - If True, force the original settings to be cleared before configuration.
        default: True
        choices: [True, False]
        required: False
    validation_files:
        description:
            - OpenApi validation files.
        required: False
    enable:
        description:
            - Set to true to enable the openapi validation.
        default: True
        choices: [True, False]
        required: False
    action:
        description:
            - Set to action of the openapi validation, only allow ["alert", "alert_deny", "deny_no_log"].
        required: True

'''
EXAMPLES = '''

'''

RETURN = '''
msg:
    description: Returns the result of the openapi validation.
    returned: always
    type: str
    sample: demo.example.com

'''


def main():
    module = AnsibleModule(
        argument_spec=dict(
            app_name=dict(type='str', required=True),
            validation_files=dict(type='list', require=False),
            force=dict(type='bool', required=False, default=True),
            enable=dict(type='bool', required=False, default=True),
            action=dict(type='str', required=True),
            api_token=dict(type='str', required=False, default=""),
        )#,
        # supports_check_mode=True
    )
    result = dict(
        changed=False,
        msg='The module was successfully executed.'
    )

    if module.check_mode:
        module.exit_json(**result)


    if module._socket_path:
        connection = Connection(module._socket_path)
        api_handler = CloudWafAPIHandler(connection, token=module.params.get("api_token"))

    else:
        module.fail_json(msg="Socket Path Empty! A persistent connection manager error occurred. Try again in a few moments.")
    
    action_list = ["alert", "alert_deny", "deny_no_log"]
    if module.params['action'] not in action_list:
        raise Exception("in valid action %s, only allow %s" %(module.params['action'], action_list))

    data = {
            "app_name": module.params['app_name'],
            "force": module.params['force'],
            "validation_files": module.params['validation_files'],
            "enable": module.params['enable'],
            "action": module.params['action'],
            "handler": api_handler,
            "api_token": module.params['api_token']
            }
    try:

        res, change = setup_openapi_validation(data=data)
        result["msg"] = res
        result["changed"] = change

    except Exception as e:
        module.fail_json(msg="During setup openapi validation, an error occurred:" + str(e))
    
    module.exit_json(**result)

if __name__ == '__main__':
    main()
