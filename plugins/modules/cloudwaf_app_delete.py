#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.app import del_app
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.fortiwebcloud import CloudWafAPIHandler

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'Fortinet'
}

DOCUMENTATION = '''
---
module: cloudwaf_app_delete
author: "Fortinet"
version_added: "2.9"
short_description: "Execute the Restful API to create the app."
description:
    - "This module will create an application on Fortiweb Cloud by the Restful API.
    Before using this module, you must be a Fortinet inc. customer."

options:
    app_name:
        description:
            -The name of the app to be deleted.
        required: True
'''
EXAMPLES = '''

'''

RETURN = '''
msg:
    description: Returns the result of the app deletion.
    returned: always
    type: str
'''


def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_token=dict(type='str', required=False, default=""),
            app_name=dict(type='str', required=True),
        ),
        supports_check_mode=True
    )
    result = dict(
        changed=False,
        msg='The module was successfully deleted.'
    )
    if module.check_mode:
        module.exit_json(**result)

    if not(module.params.get('app_name')):
        module.fail_json(msg="Required parameters must not be empty.")

    if module._socket_path:
        connection = Connection(module._socket_path)
        api_handler = CloudWafAPIHandler(connection, token=module.params.get("api_token"))

    else:
        module.fail_json(msg="Socket Path Empty! A persistent connection manager error occurred. Try again in a few moments.")

    data = {
        "app_name": module.params['app_name'],
        "handler": api_handler
    }
    try:
        del_app(data=data)

    except Exception as e:
        module.fail_json(msg="During app deletion, an error occurred:" + str(e))

    module.exit_json(changed=True, msg=f"Deletion of the app {data['app_name']} was successful.")

if __name__ == '__main__':
    main()
