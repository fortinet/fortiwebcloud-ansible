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

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'metadata_version': '1.1'}

import json
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.request import RequestBase
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.ipcheck import ServerTest, IPRegion, DnsLookup
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.template import Template
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.ipcheck import is_ip_address


class AppCreate(RequestBase):

    def __init__(self, data={}, region=None, test_result={}, template=None, handler=None):
        # def __init__(self, method='GET', path="", query='', data={}, timeout=3, **kargs):
        self.domain = data.get("domain")
        api_data = dict({"app_name": data.get("app_name", "default_app_name"),
                          "domain_name": self.domain,
                          "extra_domains": data.get("extra_domains", []),
                          "block_mode": data.get("block", 0),
                          "server_address": data.get("server"),
                          "custom_port": {},
                          "service": data.get("app_service", {}),
                          "template_enable": 0,
                          "head_availability": test_result.get("head_availability", 1),
                          "head_status_code": test_result.get("head_status_code", 200)})
        if data.get("cdn"):
            api_data["cdn_status"] = 1
            if data.get("continent_cdn"):
                api_data["is_global_cdn"] = 0
                api_data["continent"] = region.get("cluster").get("continent")
            else:
                api_data["is_global_cdn"] = 1
        else:
            api_data["cdn_status"] = 0
            api_data["server_country"] = region.get("location")
            api_data["region"] = region.get("cluster").get("single")

        if template:
            api_data["template_enable"] = 1
            api_data["template_id"] = template

        api_data["server_type"] = data.get("backend_type", "").lower()
        service = data.get("app_service", {})
        api_data["service"] = list(service.keys())
        api_data["custom_port"] = service
        platform = region.get("region", [])
        api_data["platform"] = platform[0] if len(platform) > 0 else "AWS"
        super().__init__(method='POST', path="application", data=api_data, handler=handler)

    def check(self):
        query = AppQuery(handler=self.handler, domain=self.domain)
        if query.get_ep():
            return False
        else:
            return True

    def create(self):
        return self.send()

class AppQuery(RequestBase):
    def __init__(self, domain="", app_name="", handler=None, **kwargs ):
        self.domain = domain
        self.app_name = app_name
        con = dict({"size": 1, "cursor": "", "forward": True, "filter": ""})
        url = "application"
        if domain:
            filter_con = dict(
                {"id": "domain_name", "logic": {"is": {"string": True}, "search": "string"}, "value": [domain]})
            con["filter"] = json.dumps([filter_con])
        else:
            con = dict({"partial": True})
        super().__init__(path=url, query=con, handler=handler)

    def get_ep(self):
        status, res = self.send()
        if isinstance(res, dict):
            app_list = res.get("app_list", [])
        elif isinstance(res, list):
            app_list = res
        else:
            app_list = []
        if len(app_list) > 0:
            for app in app_list:
                if app['app_name'] == self.app_name or app['domain_name'] == self.domain:
                    return app
            return None
        else:
            print("Not exist domain")
            return None

    def get_ep_id(self):
        ep = self.get_ep()
        if ep:
            return ep["ep_id"]
        else:
            return None


class AppDel(RequestBase):
    def __init__(self, handler=None, ep_id=""):
        self.ep_id = ep_id
        super().__init__(method='DELETE', path=f"application/{self.ep_id}", handler=handler)

    def del_it(self):
        self.send()
        print("Delete domain successfully")


def create_app(data={}):
    print(f"Get the data: {data}")

    template_id = None
    region = None
    server_ips = []
    query = AppQuery(app_name=data.get("app_name"), handler=data.get("handler", None))
    ep = query.get_ep()
    if ep:
        return ep, False

    template = data.get("template")
    if template.strip() != "":
        template = Template(handler=data.get("handler", None))
        template_id = template.get_id_by_name(data.get("template"))

    if not is_ip_address(data.get("server")):
        dns = DnsLookup(data.get("server"), handler=data.get("handler"))
        server_ips = dns.get_server_address()
        tester = ServerTest(server=server_ips,
                            backend_type=data.get("backend_type"), domain=data.get("domain"),
                            handler=data.get("handler", None))
    else:
        tester = ServerTest(server=data.get("server"),
                            backend_type=data.get("backend_type"), domain=data.get("domain"),
                            handler=data.get("handler", None))
    test_res = tester.pserver_test()

    region_checker = IPRegion(domain=data.get("domain"),
                              server=server_ips or data.get("server"), extra_domains=data.get("extra_domains"),
                              service=data.get("app_service"),
                              handler=data.get("handler", None))
    region = region_checker.get_ip_region()
    app = AppCreate(data=data, region=region, test_result=test_res, template=template_id,
                    handler=data.get("handler", None))
    if not app.check():  # exist app
        return {}, False
    else:
        status, res = app.create()
        print(f"create app :  status {status}, res {res}")
        if (status != 200):
            raise Exception("The application creating failure: %s" % res)
        return res, True


def del_app(data={}):
    app_name = data.get("app_name", None)
    query = AppQuery(app_name=app_name, handler=data.get("handler", None))
    ep_id = query.get_ep_id()
    if ep_id:
        app = AppDel(handler=data.get("handler", None), ep_id=ep_id)
        app.del_it()



