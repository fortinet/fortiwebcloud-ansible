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

from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.request import RequestBase
import ipaddress

class ServerTest(RequestBase):
    def __init__(self, server="", backend_type="HTTPS", domain="www.demo.com", handler=None):
        query_ip = server
        if type(server) == list:
            self.server_list = server
            query_ip = server[0]
        else:
            self.server_list = []
        self.query_data = {"backend_ip": query_ip, "backend_type": backend_type, "domain_name": domain}
        super().__init__(path="misc/backend-ip-test", query=self.query_data, handler=handler)

    def pserver_test(self):
        status, res = self.send()
        if res.get("network_connectivity", 0) == 1:
            return res
        else:
            if len(self.server_list) > 0:  # poll by cname
                for e in self.server_list[1:-1]:
                    self.query_data["backend_ip"] = e
                    status, res = self.send(data=self.query_data)
                    if res.get("network_connectivity", 0) == 1:
                        return res

            raise Exception(f"Invalid server backend: {self.server_list}!")


class DnsLookup(RequestBase):
    def __init__(self, server="", handler=None):
        api_data = {"domain": server}
        super().__init__(path="misc/dns-lookup", handler=handler, method="POST", data=api_data)

    def get_server_address(self):
        status, res = self.send()
        addresses = res.get("A", [])
        if len(addresses) > 0:
            return addresses
        else:
            raise Exception("Invalid server backend, for find server address failed!")


class IPRegion(RequestBase):
    def __init__(self, handler=None, domain="www.demo.com", server="", extra_domains=[], service={}):
        query_ip = server
        if type(server) == list:
            self.server_list = server
            query_ip = self.server_list[0]
        else:
            self.server_list = []
        self.api_data = dict({"custom_port": {}, "domain_name": domain, "extra_domains": extra_domains, "ep_ip": query_ip})
        self.api_data["custom_port"] = service
        super().__init__(path="misc/check-ip-region", method="POST", data=self.api_data, handler=handler)

    def get_ip_region(self):
        status, res = self.send()
        loc = res.get("location")
        if loc:
            print(f"Check the server belong to the country/region {loc}.")
            return res
        else:
            if len(self.server_list) > 0:  # poll by cname
                for e in self.server_list[1:-1]:
                    self.api_data["ep_ip"] = e
                    status, res = self.send(data=self.api_data)
                    if res.get("location"):
                        return res

            raise Exception(f"Invalid server backend for {self.api_data} {res}!")


def is_ip_address(val):
    try:
        ipaddress.ip_address(val)
        return True
    except Exception as e:
        return False
