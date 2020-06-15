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
import ipaddress
max_member_list_ip_value_length = 4096


def get_valid_ip(ip_db_config, can_ip_str, ip_type, name, start, end):
    db_members_list = ip_db_config.get('members', [])
    old_len = len(can_ip_str)
    can_ip_str = can_ip_str.lstrip(',')
    start = start + (old_len - len(can_ip_str))

    can_ip_list = can_ip_str.split(',')
    for index, can_ip in enumerate(can_ip_list):
        for db_member in db_members_list:
            if ip_type == db_member['type'] and can_ip in db_member['ip']:
                if int(db_member['name']) > name:
                    new_can_str = ','.join(can_ip_list[:index])
                    return new_can_str, start + len(new_can_str)
                else:
                    break
    return can_ip_str, end


def intercept_ip_list(ip_db_config, members_value):
    name_list = [int(x['name']) for x in members_value]
    max_name = max(name_list) if name_list else 0
    tmp_members = []
    delete_index = []
    for index, member in enumerate(members_value):
        ip_value = member.get('ip')
        if len(ip_value) > max_member_list_ip_value_length:
            tmp_str = ip_value[:max_member_list_ip_value_length]
            end = tmp_str.rfind(',')
            start = 0
            member['ip'], end = get_valid_ip(ip_db_config, ip_value[:end], member['type'], int(member['name']), start, end)
            if not member['ip']:
                delete_index.append(index)
            start = end
            end = start + max_member_list_ip_value_length

            while start < len(ip_value):
                tmp_member = {'type': member.get('type')}
                tmp_str = ip_value[:end]
                if start + max_member_list_ip_value_length > len(ip_value):
                    end = len(ip_value)
                else:
                    end = tmp_str.rfind(',')
                tmp_member['ip'], end = get_valid_ip(ip_db_config, ip_value[start:end], member['type'], max_name + 1,
                                                     start, end)
                max_name = max_name + 1
                if tmp_member['ip']:
                    tmp_member['name'] = str(max_name)
                    start = end
                    end = start + max_member_list_ip_value_length
                    tmp_members.append(tmp_member)
                else:
                    end = start + max_member_list_ip_value_length
        else:
            end = len(ip_value)
            start = 0
            member['ip'], end = get_valid_ip(ip_db_config, ip_value, member['type'], int(member['name']), start, end)
            if not member['ip']:
                delete_index.append(index)
            start = end
            while start < len(ip_value):
                tmp_member = {'type': member.get('type')}
                end = len(ip_value)

                tmp_member['ip'], end = get_valid_ip(ip_db_config, ip_value[start:end], member['type'], max_name + 1,
                                                     start, end)
                max_name = max_name + 1
                if tmp_member['ip']:
                    tmp_member['name'] = str(max_name)

                    start = end
                    tmp_members.append(tmp_member)
    if delete_index:
        delete_index.sort()
        for index in range(len(delete_index) - 1, -1, -1):
            del members_value[index]
    members_value = members_value + tmp_members
    return members_value


def ip_str_to_dict(old_ip_list, ip_dict):
    for index, ip in enumerate(old_ip_list):
        if '-' in ip:
            ip_start, ip_end = ip.split('-')
            int_start = int(ipaddress.ip_address(ip_start))
            int_end = int(ipaddress.ip_address(ip_end))
            new_ip_dict = {index: {'range': {'start': int_start, 'end': int_end}, 'value': ip}}

        else:
            new_ip_dict = {index: {'range': {'start': int(ipaddress.ip_address(ip)), 'end': int(ipaddress.ip_address(ip))}, 'value': ip}}
        ip_dict.update(new_ip_dict)


def deduplication(old_ip_dict, new_ip_dict):
    for key, value in old_ip_dict.items():
        add_new = True
        merged = False
        merged_new_key = None
        delete_key = []
        for new_key, new_value in new_ip_dict.items():
            if not (value['range']['end'] < new_value['range']['start'] - 1 or
                    value['range']['start'] > new_value['range']['end'] + 1):
                add_new = False

                old_start = value['range']['start']
                new_start = new_value['range']['start']
                old_end = value['range']['end']
                new_end = new_value['range']['end']
                merged_new_start = new_start
                merged_new_end = new_end
                valid_key = new_key
                if not merged:
                    merged_new_key = new_key
                    merged = True
                else:
                    delete_key.append(new_key)
                    valid_key = merged_new_key
                    merged_new_start = new_ip_dict[merged_new_key]['range']['start']
                    merged_new_end = new_ip_dict[merged_new_key]['range']['end']
                min_value = min(new_start, old_start, merged_new_start)
                max_value = max(new_end, old_end, merged_new_end)
                new_ip_dict[valid_key]['range'] = {'start': min_value, 'end': max_value}
                if min_value == max_value:
                    new_ip_dict[valid_key]['value'] = str(ipaddress.ip_address(min_value))
                else:
                    new_ip_dict[valid_key]['value'] = '%s-%s' % (str(ipaddress.ip_address(min_value)), str(ipaddress.ip_address(max_value)))
        if add_new:
            new_ip_dict.update({key: value})
        for k in delete_key:
            del new_ip_dict[k]


def dict_to_list(old_dict):
    ip_list = list(old_dict.values())
    return ip_list


def ip_dict_to_str(ip_dict):
    ip_dict_list = sorted(dict_to_list(ip_dict), key=lambda x: x['range']['start'])
    new_ip_dict_list = []
    for tmp_ip_dict in ip_dict_list:
        if tmp_ip_dict not in new_ip_dict_list:
            new_ip_dict_list.append(tmp_ip_dict)
    ip_list = [x['value'] for x in new_ip_dict_list]
    ip_str = ','.join(ip_list)
    return ip_str


def process_ip_list(ip_db_config, value):
    try:
        members_value = value.get('members', [])
        i = 1
        for member in members_value:
            member['name'] = str(i)
            i = i + 1
            ip_list = member['ip'].split(',')
            ip_dict = {}
            ip_str_to_dict(ip_list, ip_dict)
            new_ip_dict = {}
            deduplication(ip_dict, new_ip_dict)
            member['ip'] = ip_dict_to_str(new_ip_dict)

        value['members'] = intercept_ip_list(ip_db_config, members_value)
        if len(value['members']) > 256:
            raise Exception("The numbers of ip is larger.")
        return value
    except Exception as e:
        raise e
