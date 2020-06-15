#!/usr/bin/python

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2020 Fortinet, Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.request import RequestBase
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.app import AppQuery
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.common import config_is_same


class EndpointGet(RequestBase):
    def __init__(self, handler=None, ep_id=""):
        self.ep_id = ep_id
        super().__init__(path=f"application/{self.ep_id}/endpoint", handler=handler)

    def get_ep_data(self):
        res = self.send()
        return res


class EndpointUpdate(RequestBase):
    def __init__(self, data=None, handler=None, ep_id=""):
        self.ep_id = ep_id
        super().__init__(method='PUT', path=f"application/{self.ep_id}", data=data, handler=handler)

    def update_ep(self):
        res = self.send()
        return res


def update_endpoint(data=None, handler=None):
    app_name = data.get("app_name", None)
    query = AppQuery(app_name=app_name, handler=handler)
    ep_id = query.get_ep_id()
    has_changed = False
    is_error = True
    res = {"detail": "successfully"}
    if ep_id:
        endpoint_get = EndpointGet(handler=handler, ep_id=ep_id)
        old_data = endpoint_get.get_ep_data()
        not_compare_key_list = ['ep_cname', 'domain_name', 'custom_port', 'cert_auto_status', 'block_mode']
        if not data.get('custom_block_page') == 'enable':
            data.pop('block_url')
            old_data.pop('block_url')
        for key in not_compare_key_list:
            if key in old_data:
                old_data.pop(key)
        if not config_is_same(data, old_data):
            endpoint = EndpointUpdate(data=data, handler=handler, ep_id=ep_id)
            res = endpoint.update_ep()
            has_changed = True
        if res['detail'] == 'successfully':
            is_error = False

        return is_error, has_changed, res
    else:
        raise Exception("The application %s does not exist." % app_name)
