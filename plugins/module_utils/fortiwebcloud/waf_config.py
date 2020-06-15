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

import json
import copy
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.request import RequestBase
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.template import Template
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.ip_protection_process import process_ip_list
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.app import AppQuery
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.template import Template
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.common import config_is_same


class WafConfigUpdate(RequestBase):
    def __init__(self, url='', data={}, handler=None):
        url = '%s/%s' % (url, data.get('ep_id')) + "/" + data.get('module_name')
        super().__init__(method='PUT', path=url, data=data, handler=handler)

    def update(self):
        return self.send()


class WafConfigGet(RequestBase):
    def __init__(self, url='', data={}, handler=None, query={}):
        url = '%s/%s' % (url, data.get('ep_id')) + "/" + data.get('module_name')
        super().__init__(path=url, query=query, handler=handler)

    def get_data(self):
        return self.send()


def get_new_config_data(old_data, new_data):
    module_name = new_data.get('module_name')
    api_data = {'module_name': module_name, 'ep_id': new_data['ep_id']}
    if module_name == 'IPProtection':
        ip_list = new_data.get('IPProtection').get('ip-list')
        if ip_list:
            old_ip_list = old_data['IPProtection'].get('ip-list')
            new_data['IPProtection']['ip-list'] = process_ip_list(old_ip_list, ip_list)

        if not (config_is_same(new_data, old_data)):
            api_data['_status'] = new_data['_status']
            api_data['IPProtection'] = new_data['IPProtection']
            api_data['template_status'] = new_data.get('template_status', 'disable')
    return api_data


def module_support_idempotent(module_name):
    idempotent_modules = ['ipprotection']
    if module_name.lower() in idempotent_modules:
        return True
    else:
        return False


def update_waf_config(data={}, handler=None, module_name=''):
    app_name = data.get('app_name')
    temp_name = data.get('temp_name')
    if app_name:
        app_query = AppQuery(app_name=app_name, handler=handler)
        ep_id = app_query.get_ep_id()
        url = 'application'
    else:
        temp_query = Template(handler=handler)
        ep_id = temp_query.get_id_by_name(temp_name)
        url = 'template'
    has_changed = False
    is_error = True
    res = {"detail": "successfully"}
    if ep_id:
        init_con_data = {'module_name': module_name, 'ep_id': ep_id}
        new_data = data
        new_data.update(init_con_data)
        api_data = new_data
        if module_support_idempotent(module_name):
            waf_conf_get = WafConfigGet(url=url, data=init_con_data, handler=handler)
            old_data = waf_conf_get.get_data()
            api_data = get_new_config_data(old_data['result'], new_data)
        if not api_data == init_con_data:
            waf_config = WafConfigUpdate(url, api_data, handler)
            res = waf_config.update()
            has_changed = True

        if res['detail'] == 'successfully':
            is_error = False

        return is_error, has_changed, res
    else:
        if temp_name:
            raise Exception("The template %s does not exist." % temp_name)
        else:
            raise Exception("The application %s does not exist." % app_name)


def get_waf_config(data={}, handler=None, module_name='', query={}):
    app_name = data.get('app_name')
    temp_name = data.get('temp_name')
    if app_name:
        app_query = AppQuery(app_name=app_name, handler=handler)
        ep_id = app_query.get_ep_id()
        url = 'application'
    else:
        temp_query = Template(handler=handler)
        ep_id = temp_query.get_id_by_name(temp_name)
        url = 'template'
    has_changed = False
    is_error = True
    res = {}
    if ep_id:
        init_con_data = {'module_name': module_name, 'ep_id': ep_id}
        data.update(init_con_data)
        waf_config = WafConfigGet(url, data, handler, query)
        res = waf_config.get_data()
        is_error = False
    return is_error, has_changed, res

