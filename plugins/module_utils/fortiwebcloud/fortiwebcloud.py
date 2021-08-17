
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

import json

# BEGIN HANDLER CLASSES
class CloudWafAPIHandler(object):
    def __init__(self, conn, token=""):
        self._conn = conn
        self.by_token = False
        if token != "":
            self.by_token = True
            self.token = token

    def send_req(self, url, data="", files=None, headers={}, method="GET"):
        if self.by_token:
            headers["Authorization"] = "Basic " + self.token
        status, result_data = self._conn.send_request(url=url, data=data, files=files, headers=headers, method=method)
        return status, result_data


    @staticmethod
    def return_response(module, results, msg="NULL", good_codes=(0,),
                        stop_on_fail=True, stop_on_success=False, skipped=False,
                        changed=False, unreachable=False, failed=False, success=False, changed_if_success=True,
                        ansible_facts=()):
        """
        This function controls logout and error reporting after a method or function runs. The exit_json for ansible comes from logic within this function. If this function returns just the msg, it means to continue execution on the playbook. It is called from the ansible module, or from the self.govern_response function.

        :param module: The Ansible Module CLASS object, used to run fail/exit json.
        :type module: object
        :param msg: An overridable custom message from the module that called this.
        :type msg: string
        :param results: A dictionary object containing an API call results.
        :type results: dict
        :param good_codes: A list of exit codes considered successful from fortiwebcloud.
        :type good_codes: list
        :param stop_on_fail: If true, stops playbook run when return code is NOT IN good codes (default: true).
        :type stop_on_fail: boolean
        :param stop_on_success: If true, stops playbook run when return code is IN good codes (default: false).
        :type stop_on_success: boolean
        :param changed: If True, tells Ansible that object was changed (default: false).
        :type skipped: boolean
        :param skipped: If True, tells Ansible that object was skipped (default: false).
        :type skipped: boolean
        :param unreachable: If True, tells Ansible that object was unreachable (default: false).
        :type unreachable: boolean
        :param failed: If True, tells Ansible that execution was a failure. Overrides good_codes. (default: false).
        :type unreachable: boolean
        :param success: If True, tells Ansible that execution was a success. Overrides good_codes. (default: false).
        :type unreachable: boolean
        :param changed_if_success: If True, defaults to changed if successful if you specify or not."
        :type changed_if_success: boolean
        :param ansible_facts: A prepared dictionary of ansible facts from the execution.
        :type ansible_facts: dict

        :return: A string object that contains an error message.
        :rtype: str
        """

        # VALIDATION ERROR
        if (len(results) == 0) or (failed and success) or (changed and unreachable):
            module.exit_json(msg="Handle_response was called with no results, or conflicting failed/success or "
                                 "changed/unreachable parameters. Fix the exit code on module. "
                                 "Generic Failure", failed=True)

        # IDENTIFY SUCCESS/FAIL IF NOT DEFINED
        if not failed and not success:
            if len(results) > 0:
                if results[0] not in good_codes:
                    failed = True
                elif results[0] in good_codes:
                    success = True

        if len(results) > 0:
            # IF NO MESSAGE WAS SUPPLIED, GET IT FROM THE RESULTS, IF THAT DOESN'T WORK, THEN WRITE AN ERROR MESSAGE
            if msg == "NULL":
                try:
                    msg = results[1]['status']['message']
                except BaseException:
                    msg = "No status message returned at results[1][status][message], " \
                          "and none supplied to msg parameter for handle_response."

            if failed:
                # BECAUSE SKIPPED/FAILED WILL OFTEN OCCUR ON CODES THAT DON'T GET INCLUDED, THEY ARE CONSIDERED FAILURES
                # HOWEVER, THEY ARE MUTUALLY EXCLUSIVE, SO IF IT IS MARKED SKIPPED OR UNREACHABLE BY THE MODULE LOGIC
                # THEN REMOVE THE FAILED FLAG SO IT DOESN'T OVERRIDE THE DESIRED STATUS OF SKIPPED OR UNREACHABLE.
                if failed and skipped:
                    failed = False
                if failed and unreachable:
                    failed = False
                if stop_on_fail:
                    module.exit_json(msg=msg, failed=failed, changed=changed, unreachable=unreachable, skipped=skipped,
                                     results=results[1], ansible_facts=ansible_facts, rc=results[0],
                                     invocation={"module_args": ansible_facts["ansible_params"]})
            elif success:
                if changed_if_success:
                    changed = True
                    success = False
                if stop_on_success:
                    module.exit_json(msg=msg, success=success, changed=changed, unreachable=unreachable,
                                     skipped=skipped, results=results[1], ansible_facts=ansible_facts, rc=results[0],
                                     invocation={"module_args": ansible_facts["ansible_params"]})
        return msg
