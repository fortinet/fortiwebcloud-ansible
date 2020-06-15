#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.fortiwebcloud import CloudWafAPIHandler

from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.app import create_app

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'Fortinet'
}

DOCUMENTATION = '''
---
module: cloudwaf_app_create
author: "Fortinet"
version_added: "2.9"
short_description: "Execute the Restful API to create the app."
description:
    - "This module will create an application on Fortiweb Cloud by the Restful API.
    Before using this module, you must be a Fortinet inc. customer."

options:
    app_name:
        description:
            - Any name you want for your app.
        required: True
    domain_name:
        description:
            - The domain name you want protected.
        required: True
    origin_server_ip:
        description:
            - The IP address of your domain server.
        required: True
    app_service:
        description:
            - The service port WAF should support.
        default: http: 80, https: 443
        required: True
    extra_domains:
        description:
            - Your domains' other names.
        default: []
        required: False
    origin_server_service:
        description:
            - The service your server provides.
        default: HTTPS
        required: False
    cdn:
        description:
            - Set to true to enable the CDN.
        default: False
        choices: [True, False]
        required: False
    block:
        description:
            - Set to true to enable block mode for your app.
        default: False
        required: False
    template:
        description:
            - The template name
            - To bind a template during app creation, specify the template name.
        required: False
'''
EXAMPLES = '''

'''

RETURN = '''
msg:
    description: The new alias name for your domain, you should change your domain's server address to this address on the DNS.
    returned: always
    type: str
    sample: demo.example.com

'''


def main():
    module = AnsibleModule(
        argument_spec=dict(
            app_name=dict(type='str', required=True),
            domain_name=dict(type='str', required=True),
            extra_domains=dict(type='list', require=False, default=[]),
            app_service=dict(type='dict', require=True),
            origin_server_ip=dict(type='str', required=True),
            origin_server_service=dict(type='str', required=False, default="HTTPS"),
            origin_server_port=dict(type='int', required=False, default=443),
            cdn=dict(type='bool', required=False, default=False),
            block=dict(type='bool', required=False, default=False),
            template=dict(type='str', required=False, default=""),
            api_token=dict(type='str', required=False, default=""),
        ),
        supports_check_mode=True
    )
    result = dict(
        changed=False,
        msg='The module was successfully executed.'
    )

    if module.check_mode:
        module.exit_json(**result)

    app_service = module.params.get("app_service")
    if not app_service.get("http") and not app_service.get("https"):
        module.fail_json(msg="You must specify the http port or https port.")

    if not(module.params.get('app_name') and module.params.get('domain_name') and
            module.params.get('origin_server_ip')):
        module.fail_json(msg="Required parameters must not be empty.")

    if module._socket_path:
        connection = Connection(module._socket_path)
        api_handler = CloudWafAPIHandler(connection, token=module.params.get("api_token"))

    else:
        module.fail_json(msg="Socket Path Empty! A persistent connection manager error occurred. Try again in a few moments.")

    data = {
            "app_name": module.params['app_name'],
            "domain": module.params['domain_name'],
            "extra_domains": module.params['extra_domains'],
            "app_service": module.params['app_service'],
            "server": module.params['origin_server_ip'],
            "backend_type": module.params['origin_server_service'],
            "port": module.params['origin_server_port'],
            "cdn": module.params['cdn'],
            "block": 1 if module.params['block'] else 0,
            "template": module.params['template'],
            "handler": api_handler
            }
    try:
        res, change = create_app(data=data)
        result["msg"] = json.dumps(res)
        result["changed"] = change

    except Exception as e:
        module.fail_json(msg="During app creation, an error occurred:" + str(e))

    module.exit_json(**result)

if __name__ == '__main__':
    main()
