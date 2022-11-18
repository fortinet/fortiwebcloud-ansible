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

import os
import re
import json
import time

import threading
import urllib.parse

from ansible.plugins.httpapi import HttpApiBase
from ansible.module_utils.basic import to_text
from ansible.module_utils.six.moves import urllib
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.settings import (API_VER, DOMAIN)

# Global FWB REST connection session

class RequestBase(object):
    def __init__(self, method='GET', path="", query='', data={}, files=None, handler=None, timeout=60, **kargs):
        self.method = method
        self.data = data
        self.files = files
        self.timeout = timeout

        if type(query) == "string":
            self.query = query
        else:
            self.query = urllib.parse.urlencode(query)

        self.api_ver = API_VER
        self.domain = DOMAIN
        self.path = path
        self.url = self._set_url()

        self.headers = dict()

        self.set_headers('Content-Type', 'application/json')
        self.set_headers('Accept', 'text/plain')
        self.handler = handler

    @staticmethod
    def _format_path(path):
        return '/'.join([seg for seg in path.split('/') if len(seg)])

    def _set_url(self):
        ulist = []
        ulist.append(self.api_ver)
        ulist.append(self.path)
        url = "/".join(ulist)
        if self.query:
            query_str = self.query if self.query.startswith('?') else '?' + self.query
            url = url + query_str
        return "/" + url

    def set_headers(self, key, value):
        self.headers[key] = value

    def validate(self):
        """
        Validate the setup of rest api
        """
        if not self.method in ('GET', 'POST', 'PUT', 'DELETE'):
            raise Exception("REST API method %s not supported." % self.method)

    def get(self, data={}):
        status, res = self.handler.send_req(self.url, headers=self.headers, method="GET")
        return status, res

    def delete(self, data={}):
        status, res = self.handler.send_req(self.url, headers=self.headers, method="DELETE")
        return status, res

    def put(self, data={}, files=None):
        status, res = self.handler.send_req(
            self.url, headers=self.headers, 
            data=json.dumps(data), files=files, method="PUT")
        return status, res

    def post(self, data={}):
        status, res = self.handler.send_req(
            self.url, headers=self.headers,
            data=json.dumps(data), method="POST")
        return status, res

    def send(self, data=None, files=None):
        """
        Send rest api, and wait its return.
        """
        self.validate()

        try:
            ts = time.time()

            method_val = getattr(self, self.method.lower(), self.get)
            d = data or self.data
            print(f"send data {d}")
            f = files or self.files
            print(f"send files {f}")
            if f:
                status, response = method_val(data=d, files=f)
            else:
                status, response = method_val(data=d)
            try:
                response = json.loads(response)
            except Exception as e:
                raise Exception(f"Get response json content failed for {e}.")
            duration = time.time() - ts
            print(f"URL:{self.url}, method:{self.method} finished, status:{status} duration:{duration}.")
            return status, response
        except Exception as e:
            raise Exception("Failed to connect to %s: %s." % (self.url, e))
