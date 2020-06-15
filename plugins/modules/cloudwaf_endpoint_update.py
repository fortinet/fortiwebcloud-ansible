#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.fortiwebcloud import CloudWafAPIHandler
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.endpoint import update_endpoint

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'Fortinet'
}

DOCUMENTATION = '''
---
module: cloudwaf_endpoint_update
author: "Fortinet"
version_added: "2.9"
short_description: "Execute the Restful API to update the endpoint."
description:
    - "This module will update an application on Fortiweb Cloud by the Restful API.
    Before using this module, you must be a Fortinet inc. customer."

options:
    app_name:
        description:
            - The name of the application you want to configure.
        required: True
        type: str
    http_status:
        description:
            - HTTP configuration. Set to 1 to enable, 0 to disable.
        type: int
        required: False
        choices:
            - 0
            - 1
    https_status:
        description:
            - HTTPS configuration. Set to 1 to enable, 0 to disable.
        type: int
        required: False
        choices:
            - 0
            - 1
    ipv6_option:
        description:
            - IPv6 configuration. Set to 1 to enable, 0 to disable.
        type: int
        required: False
        choices:
            - 0
            - 1
    custom_http_port:
        description:
            - Configure a custom port as http service port.
        type: int
        required: False
        default: 80
    custom_https_port:
        description:
            - Configure a custom port as https service port.
        type: int
        required: False
        default: 443
    http2_status:
        description:
            - HTTP2 configuration. Set to 1 to enable, 0 to disable.
        required: False
        type: int
        choices:
            - 0
            - 1
        default: 0
    extra_domains:
        description:
            - Extra domain names.
        default: []
        required: False
        type: list
    cert_type:
        description:
            - Certificate configuration. Set to 1 for automatic, 0 for custom.
        required: False
        type: int
        choices:
            - 0
            - 1
    ssl_options:
        description:
            - Configure SSL options.
        required: False
        type: dict
        suboptions:
            tls_1_0:
                description:
                    - TLS configuration. Set to 1 to enable, 0 to disable.
                required: False
                type: int
                choices:
                    - 0
                    - 1
            tls_1_1:
                description:
                    - TSL 1.1 configuration. Set to 1 to enable, 0 to disable.
                required: False
                type: int
                choices:
                    - 0
                    - 1
            tls_1_2:
                description:
                    - TSL 1.2 configuration. Set to 1 to enable, 0 to disable.
                required: False
                type: int
                choices:
                    - 0
                    - 1
            tls_1_3:
                description:
                    - TSL 1.3 configuration. Set to 1 to enable, 0 to disable.
                required: False
                type: int
                choices:
                    - 0
                    - 1
            encryption_level:
                description:
                    - Configure to only allow other level ciphers or only allow strong ciphers.
                required: False
                type: int
                choices:
                    - 1
                    - 2
            http_2_https:
                description:
                    - HTTP traffic to HTTPS configuration. Set to 1 to enable, 0 to disable.
                required: False
                type: int
                choices:
                    - 0
                    - 1
    custom_block_page:
        description:
            - Configure to disable or enable the custom block page.
        required: False
        type: str
        choices:
            - enable
            - disable
        default: disable
    block_url:
        description:
            - Configure the URL of the custom block page (start with '/').
        required: False
        type: str
'''
EXAMPLES = '''
---

- name: Execute cloud api
  hosts: fortiwebcloud01
  gather_facts: no
  collections:
    - fortinet.fortiwebcloud
  connection: httpapi
  vars:
    ansible_httpapi_validate_certs: False
    ansible_httpapi_use_ssl: true
    ansible_httpapi_port: 443
    application_name:  "YOUR_APP_NAME"
  tasks:
    - name: Update an endpoint.
      cloudwaf_app_update:
        app_name: "{{application_name}}"
        http_status: 1
        https_status: 1
        http2_status: 0
        ipv6_option: 0
        extra_domains: []
        cert_type: 1
        ssl_options:
          tls_1_0: 0
          tls_1_1: 0
          tls_1_2: 1
          tls_1_3: 1
          encryption_level: 2
          http_2_https: 1
        custom_block_page: disable
        block_url: ''
        custom_http_port: 80
        custom_https_port: 443

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
            api_token=dict(type='str', required=False, default=""),
            app_name=dict(type='str', required=True),
            http_status=dict(type='int', required=False, choices=[0, 1]),
            https_status=dict(type='int', required=False, choices=[0, 1]),
            ipv6_option=dict(type='int', required=False, choices=[0, 1]),
            custom_http_port=dict(type='int', required=False, default=80),
            custom_https_port=dict(type='int', required=False, default=443),
            http2_status=dict(type='int', required=False, choices=[0, 1], default=0),
            extra_domains=dict(type='list', require=False, default=[]),
            cert_type=dict(type='int', required=False, choices=[0, 1]),
            ssl_options=dict(required=False, type='dict',
                             options=dict(tls_1_0=dict(required=False, type='int', choices=[0, 1]),
                                          tls_1_1=dict(required=False, type='int', choices=[0, 1]),
                                          tls_1_2=dict(required=False, type='int', choices=[0, 1]),
                                          tls_1_3=dict(required=False, type='int', choices=[0, 1]),
                                          encryption_level=dict(required=False, type='int', choices=[1, 2]),
                                          http_2_https=dict(required=False, type='int', choices=[0, 1]))),
            custom_block_page=dict(type='str', required=False, choices=['enable', 'disable'], default='disable'),
            block_url=dict(type='str', required=False)
        ),
        supports_check_mode=True
    )
    result = dict(
        changed=False,
        msg='The module was successfully executed.'
    )

    if module.check_mode:
        module.exit_json(**result)

    api_handler = None
    if module._socket_path:
        connection = Connection(module._socket_path)
        api_handler = CloudWafAPIHandler(connection, token=module.params.get("api_token"))

    else:
        module.fail_json(msg="Socket Path Empty! The persistent connection manager is messed up. Try again in a few moments.")

    data = copy.deepcopy(module.params)
    try:
        is_error, changed, res = update_endpoint(data=data, handler=api_handler)
        if not is_error:
            result["meta"] = res
            result["changed"] = changed
            module.exit_json(**result)
        else:
            result["meta"] = res
            result["msg"] = "Error in repo."
            module.fail_json(**result)

    except Exception as e:
        module.fail_json(msg="While updating the app, an error occurred:" + str(e))

if __name__ == '__main__':
    main()
