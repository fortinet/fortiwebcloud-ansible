#!/usr/bin/python

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2021 Fortinet, Inc
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

import os
import requests
import json
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.request import RequestBase
from ansible_collections.fortinet.fortiwebcloud.plugins.module_utils.fortiwebcloud.app import AppQuery

class OpenApiValation(RequestBase):
    def __init__(self, force=True, handler=None, ep_id="", validation_files=[], enable=True, action="", api_token=""):
        data = {
            "action":action,
            "OpenAPIValidationPolicy":{"schema-file":[]}
        }
        self.force = force
        self.validation_files = validation_files
        self.ep_id = ep_id
        self.enable = False if enable == False else True
        self.api_token = api_token
        self.action = action
        super().__init__(method='PUT', path=f"application/{self.ep_id}/apiprotection", data=data, handler=handler)


    def del_all(self):
        self.data = {
            "action":self.action,
            "OpenAPIValidationPolicy":{"schema-file":[
            ]}
        }
        ret = self.send()
        if(ret != None and ret.get("detail") == "successfully"):
            print("Empty OpenApi Validation successfully")
        else:
            raise Exception(ret)

    def do_setup_openapi_validation(self):
        if self.force == True:
            self.del_all()
        files = []
        schema_file = []
        i = 1
        for file in self.validation_files:
            files.append({"name": "file_"+str(i), "path": file})
            schema_file.append({"openapi-file": os.path.basename(file), "seq": str(i)})
            i+=1
        status = "enable" if self.enable else "disable"
        try:
            self.data = {
                "action":self.action,
                "OpenAPIValidationPolicy":{"schema-file":schema_file},
                "_status": status
            }
            self.files = files
            response_text = self.send()
            return response_text
        except Exception as e:
            raise Exception(e)


def setup_openapi_validation(data={}):
    api_handler = data.get("handler", None)
    api_token = data.get("api_token", None)
    force = data.get("force", None)
    enable = data.get("enable", None)
    action = data.get("action", None)
    validation_files=data.get("validation_files", [])
    app_name = data.get("app_name", None)
    query = AppQuery(app_name=app_name, handler=data.get("handler", None))
    ep_id = query.get_ep_id()
    if ep_id:
        module = OpenApiValation(handler=api_handler, force=force, ep_id=ep_id, validation_files=validation_files, api_token=api_token, enable=enable, action=action)
        response_text = module.do_setup_openapi_validation()
        if(response_text != None and response_text.get("detail") == "successfully"):
            return "Setup OpenApi Validation successfully", True
        else:
            raise Exception(f"setup openapi validation fail: " + str(response_text))