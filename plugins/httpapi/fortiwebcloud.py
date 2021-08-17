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

DOCUMENTATION = """
---
author:
    - fortiweb(@fortinet.com)
httpapi : fortiwebcloud
short_description: HttpApi Plugin for FortiwebCloud Application.
description:
  - This HttpApi plugin provides methods to connect to FortiwebCloud via REST API.
version_added: "2.9"
"""
import os
import json
import requests
from ansible.module_utils.six.moves.urllib.parse import urlencode
from ansible.plugins.httpapi import HttpApiBase
from ansible.module_utils.basic import to_text
from datetime import datetime

class HttpApi(HttpApiBase):
    def __init__(self, connection):
        super(HttpApi, self).__init__(connection)
        self._log = open("/tmp/fortiwebcloud.ansible.log", "a")
        self._token = ""
        self.by_token = False

    def log(self, msg):
        if os.path.exists("/var/log/cloudwaf-debug"):
            log_message = str(datetime.now())
            log_message += ": " + str(msg) + '\n'
            self._log.write(log_message)
            self._log.flush()

    def set_become(self, become_context):
        """
        Elevation is not required on Fortinet  - Skipped
        :param become_context: Unused input.
        :return: None
        """
        return None

    def login(self, username, password):
        """Call a defined login endpoint to receive an authentication token."""

        if username is None:
            self.by_token = True
            return   # we assume you are login by access key
        self.log("login begin, user: %s" % (username))
        data = dict({
            "username": username,
            "password": password

        })
        #data["group"] = "C8"


        dummy, result_data = self.send_request(url='/v1/token', data=json.dumps(data), method='POST')

        result_data = json.loads(result_data)
        if not result_data.get("token", None):
            raise Exception('Wrong FortiwebCloud username or password. Please check.')

    def logout(self):
        """ Call to implement session logout."""
        # not need logout
        pass

    def update_auth(self, response, response_text):
        """
        Get cookies and obtain value for csrftoken that will be used on next requests.
        :param response: Response given by the server.
        :param response_text Unused_input.
        :return: Dictionary containing headers.
        """

        headers = {}
        try:
            headers['Content-Type'] = 'application/json'
            headers['Accept'] = 'text/plain'
            if self.by_token:
                return headers
            elif self._token:
                headers["Authorization"] = self._token
            else:
                res = json.loads(to_text(response_text.getvalue()))
                headers["Authorization"] = res.get('token')
                self._token = res.get('token')

        except Exception as e:
            self.log(f"invalid user access for {e}.")
        self.log(f"set request header: {headers}.")
        return headers

    def handle_httperror(self, exc):
        """
        Not required on Fortinet - Skipped
        :param exc: Unused input.
        :return: exc
        """
        return exc

    def send_request(self, **message_kwargs):
        """
        Responsible for actual sending of data to the connection httpapi base plugin.
        :param message_kwargs: A formatted dictionary containing request info: url, data, method.

        :return: Status code and response data.
        """
        url = message_kwargs.get('url', '/')
        data = message_kwargs.get('data', '')
        method = message_kwargs.get('method', 'GET')
        headers = message_kwargs.get("headers")
        files = message_kwargs.get("files")
        self.log(f"url {url} send data: {data}")
        self.log(f"header: {headers}")
        self.log(f"files: {files}")
        f=[]
        payload={}
        if files:
            if not self.by_token:
                headers = self.connection._auth
            del headers['Content-Type']
            
            self.log(f"send data header: {headers}")
            for file in files:
                f.append((file.get("name"), (os.path.basename(file.get("path")), open(file.get("path"), 'rb'), 'application/octet-stream')))
            for k, v in json.loads(data).items():
                if type(v) is str:
                    payload[k] = v
                else:
                    payload[k]=json.dumps(v)
            response = requests.request(method, self.connection._url + url, headers=headers, data=payload, files=f)
            self.log(f"url {self.connection._url + url} get response status: {response.status_code}.")
            self.log(f"url {url} get response data: {response.text}.")
            return response.status_code, to_text(response.text)
        else:
            try:
                response, response_data = self.connection.send(url, data, method=method, headers=headers)
                self.log(f"url {url} get response status: {response.status}.")
                self.log(f"url {url} get response data: {response_data.getvalue()}.")
                return response.status, to_text(response_data.getvalue())
            except Exception as err:
                self.log(f"url {url} error happend: {err}.")
                raise Exception(err)
