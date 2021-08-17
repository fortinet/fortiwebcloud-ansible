![](https://www.fortiweb-cloud.com/styles/img/fortinet_logo.svg#align=left&display=inline&height=39&margin=%5Bobject%20Object%5D&originHeight=39&originWidth=320&status=done&style=none&width=320)

## FortiWeb Cloud Ansible Collection

The collection is the FortiWeb Cloud Ansible Automation project. It includes the modules that configure FortiWeb Cloud by allowing the user to configure WAF (Web Application Firewall) features.

## Requirements

- Ansible 2.9+ (to support the newer Ansible Collections format)
- Python 3.6+

## Installation

This collection can be downloaded from [ansible-galaxy](https://galaxy.ansible.com/), with installation steps as follows:

1. Install or upgrade to Ansible 2.9+.
2. Install the collection with the command `ansible-galaxy collection install fortinet.fortiwebcloud:1.0.2`.

## Supported FortiWeb Cloud Versions
| FortiWeb Cloud Version | Galaxy  Version | Release Date | Install Path |
| --- | :---: | :---: | :---: |
| 21.3.b | `latest` | 2021/8/30 | `ansible-galaxy collection install fortinet.fortiwebcloud:1.0.2` |

## Compatibility
This integration has been tested against Ansible version 2.9.6. Versions above this are expected to work but have not been tested.
## Modules

| Module Name | Description |
| --- | :---: |
| cloudwaf_app_create | Onboard an application in Fortinet's FortiWeb Cloud. |
| cloudwaf_app_delete | Delete an application from Fortinet's FortiWeb Cloud. |
| cloudwaf_ip_protection_method | Configure IP Protection settings in Fortinet's FortiWeb Cloud. |
| cloudwaf_endpoint_update | Modify the endpoint configuration of the application. |
| cloudwaf_inter_cert_method | Configure intermediate certificates for the application. |
| cloudwaf_sni_cert_method | Configure SNI certificates for the application. |
| cloudwaf_openapi_validation | Configure Openapi Validation for the application. |

## Usage

More information about the usage can be found in [Fortinet's FortiWeb Cloud Online Help](https://docs.fortinet.com/document/fortiweb-cloud/latest/user-guide/956788/configuring-fortiweb-cloud-with-ansible).

**Example to create an application in Fortinet's FortiWeb Cloud**

1. Create `fwbcld_app_create.yml` with the following template:

    ```yaml
    ---
    - hosts: fortiwebcloud01
      collections:
        - fortinet.fortiwebcloud
      connection: httpapi
      vars:
        application_name:  "YOUR_APP_NAME"
        ansible_httpapi_validate_certs: False
        ansible_httpapi_use_ssl: true
        ansible_httpapi_port: 443
      tasks:
        - name: Create an application.
          cloudwaf_app_create:
            app_name: "{{application_name}}"
            domain_name: "www.demo.com"
            extra_domains:
              - a.example.com
              - b.example.com
            app_service:
              http: 80
              https: 443
            origin_server_ip: "166.111.4.100"
            origin_server_service: "HTTPS"
            origin_server_port: "443"
            cdn: False
            block: False
            template: "your-template-name-or-empty"
    ```

2. Create the `hosts` inventory file:

    ```
    [fortiwebcloud]
    fortiwebcloud01 ansible_host="api.fortiweb-cloud.com" ansible_user="Your Account" ansible_password="Your Password"

    [fortiwebcloud:vars]
    ansible_network_os=fortinet.fortiwebcloud.fortiwebcloud
    ```

3. Run the test:

    ```bash
    ansible-playbook fwbcld_app_create.yml -i hosts  -e 'ansible_python_interpreter=/usr/bin/python3'
    ```

**Example to delete an existing application in Fortinet's FortiWeb Cloud**

1. Create `fwbcld_app_delete.yml` with the following template:

    ```yaml
    ---
    - hosts: fortiwebcloud01
      gather_facts: no
      collections:
        - fortinet.fortiwebcloud
      connection: httpapi
      vars:
        ansible_httpapi_validate_certs: False
        ansible_httpapi_use_ssl: True
        ansible_httpapi_port: 443
        application_name:  "YOUR_APP_NAME"
      tasks:
      - name: Delete the application.
        cloudwaf_app_delete:
          app_name: "{{application_name}}"
    ```

2. Create the `hosts` inventory file:

    ```
    [fortiwebcloud]
    fortiwebcloud01 ansible_host="api.fortiweb-cloud.com" ansible_user="Your Account" ansible_password="Your Password"

    [fortiwebcloud:vars]
    ansible_network_os=fortinet.fortiwebcloud.fortiwebcloud
    ```

3. Run the test:

    ```bash
    ansible-playbook fwbcld_app_delete.yml -i hosts  -e 'ansible_python_interpreter=/usr/bin/python3'
    ```

**Example to configure IP Protection attributes in Fortinet's FortiWeb Cloud**

1. Create `fwbcld_app_ip_set.yml` with the following template:

    ```yaml
    ---
    - hosts: fortiwebcloud01
      name: Execute cloud api
      collections:
        - fortinet.fortiwebcloud
      gather_facts: no
      connection: httpapi
      vars:
        ansible_httpapi_validate_certs: False
        ansible_httpapi_use_ssl: True
        ansible_httpapi_port: 443
        application_name:  "YOUR_APP_NAME"
      tasks:
      - name: Configure IP Protection.
        cloudwaf_ip_protection_method:
        app_name: "{{application_name}}"
        template_status: disable
        _status: enable
        IPProtection:
          ip-reputation: enable
          geo-ip-block:
          members:
            - Antigua And Barbuda
            - Aland Islands
            - Afghanistan
          ip-list:
          members:
            - type: trust-ip
            ip: '1.1.1.1,2.2.2.21-2.2.2.27'
            - type: block-ip
            ip: '3.1.1.1,3.1.1.11-3.1.1.17'
            - type: allow-only-ip
            ip: '4.1.1.1-4.1.1.17,4.1.1.19'
    ```

2. Create the `hosts` inventory file:

    ```
    [fortiwebcloud]
    fortiwebcloud01 ansible_host="api.fortiweb-cloud.com" ansible_user="Your Account" ansible_password="Your Password"

    [fortiwebcloud:vars]
    ansible_network_os=fortinet.fortiwebcloud.fortiwebcloud
    ```

3. Run the test:

    ```bash
    ansible-playbook fwbcld_app_delete.yml -i hosts  -e 'ansible_python_interpreter=/usr/bin/python3'
    ```

**Example to create an application with custom certificate in Fortinet's FortiWeb Cloud**

1. Create `fwbcld_app_with_custom_cert.yml` with the following template:

   ```yaml
   ---
   - hosts: fortiwebcloud01
     collections:
       - fortinet.fortiwebcloud
     connection: httpapi
     vars:
       application_name:  "YOUR_APP_NAME"
       ansible_httpapi_validate_certs: False
       ansible_httpapi_use_ssl: true
       ansible_httpapi_port: 443
     tasks:
       - name: Create an application.
         cloudwaf_app_create:
           app_name: "{{application_name}}"
           domain_name: "www.demo.com"
           extra_domains:
             - a.example.com
             - b.example.com
           app_service:
             http: 80
             https: 443
           origin_server_ip: "166.111.4.100"
           origin_server_service: "HTTPS"
           origin_server_port: "443"
           cdn: False
           block: False
           template: "your-template-name-or-empty"
       - name: sleep 120 seconds for the added app take effect
         wait_for:
           timeout: 120
         delegate_to: localhost
       - name: Update an application.
         cloudwaf_endpoint_update:
           app_name: "{{application_name}}"
           http_status: 1
           https_status: 1
           http2_status: 1
           extra_domains: [a.example.com, b.example.com]
           cert_type: 1
           ssl_options:
             tls_1_0: 0
             tls_1_1: 0
             tls_1_2: 1
             tls_1_3: 1
             encryption_level: 1
             http_2_https: 1
           custom_block_page: enable
           block_url: ''
           custom_http_port: 80
           custom_https_port: 443
       - name: Configure intermediate certificates.
         cloudwaf_inter_cert_method:
           app_name: "{{application_name}}"
           action: import
           certificate: |
             -----BEGIN CERTIFICATE-----
             Your intermediate certificate
             -----END CERTIFICATE-----
       - name: Import SNI certificate.
         cloudwaf_sni_cert_method:
           app_name: "{{application_name}}"
           action: import
           certificate: |
             -----BEGIN CERTIFICATE-----
             Your certificate
             -----END CERTIFICATE-----
           private_key: |
             -----BEGIN RSA PRIVATE KEY-----
             Your private key of the certificate
             -----END RSA PRIVATE KEY-----
           passwd: "Your password"
       - name: sleep 120 seconds to make sure the configuration take effect
         wait_for:
           timeout: 120
         delegate_to: localhost
   ```

2. Create the `hosts` inventory file:

   ```
   [fortiwebcloud]
   fortiwebcloud01 ansible_host="api.fortiweb-cloud.com" ansible_user="Your Account" ansible_password="Your Password"
   [fortiwebcloud:vars]
   ansible_network_os=fortinet.fortiwebcloud.fortiwebcloud
   ```

3. Run the test:

   ```bash
   ansible-playbook fwbcld_app_create.yml -i hosts  -e 'ansible_python_interpreter=/usr/bin/python3'
   ```

**Example to delete the custom certificate and import a new one in Fortinet's FortiWeb Cloud**

1. Create `fwbcld_app_with_custom_cert.yml` with the following template:

   ```yaml
   ---
   - hosts: fortiwebcloud01
     collections:
       - fortinet.fortiwebcloud
     connection: httpapi
     vars:
       application_name:  "YOUR_APP_NAME"
       ansible_httpapi_validate_certs: False
       ansible_httpapi_use_ssl: true
       ansible_httpapi_port: 443
     tasks:
       - name: Get the SNI certificates.
         cloudwaf_sni_cert_method:
           app_name: "{{application_name}}"
           action: get
         register: sni_cert_id
       - name: Delete SNI certificates.
         cloudwaf_sni_cert_method:
           app_name: "{{application_name}}"
           action: delete
           id: "{{ item.id }}"
         with_items:
           - "{{ sni_cert_id.meta }}"
       - name: Get intermediate certificates.
         cloudwaf_inter_cert_method:
           app_name: "{{application_name}}"
           action: get
         register: inter_cert_id
       - name: Delete Intermediate certificates.
         cloudwaf_inter_cert_method:
           app_name: "{{application_name}}"
           action: delete
           id: "{{ item.id }}"
         with_items:
           - "{{inter_cert_id.meta}}"
       - name: sleep 120 seconds for the added app take effect
         wait_for:
           timeout: 120
         delegate_to: localhost
       - name: Update an application.
         cloudwaf_endpoint_update:
           app_name: "{{application_name}}"
           http_status: 1
           https_status: 1
           http2_status: 1
           cert_type: 1
           ssl_options:
             tls_1_0: 0
             tls_1_1: 0
             tls_1_2: 1
             tls_1_3: 1
             encryption_level: 1
             http_2_https: 1
           custom_block_page: enable
           block_url: ''
           custom_http_port: 80
           custom_https_port: 443
       - name: Import intermediate certificate.
         cloudwaf_inter_cert_method:
           app_name: "{{application_name}}"
           action: import
           certificate: |
             -----BEGIN CERTIFICATE-----
             Your intermediate certificate
             -----END CERTIFICATE-----
       - name: Import SNI certificate.
         cloudwaf_sni_cert_method:
           app_name: "{{application_name}}"
           action: import
           certificate: |
             -----BEGIN CERTIFICATE-----
             Your certificate
             -----END CERTIFICATE-----
           private_key: |
             -----BEGIN RSA PRIVATE KEY-----
             Your private key of the certificate
             -----END RSA PRIVATE KEY-----
           passwd: "Your password"
       - name: sleep 120 seconds to make sure the configuration take effect
         wait_for:
           timeout: 120
         delegate_to: localhost
   ```

2. Create the `hosts` inventory file:

   ```
   [fortiwebcloud]
   fortiwebcloud01 ansible_host="api.fortiweb-cloud.com" ansible_user="Your Account" ansible_password="Your Password"
   [fortiwebcloud:vars]
   ansible_network_os=fortinet.fortiwebcloud.fortiwebcloud
   ```

3. Run the test:

   ```bash
   ansible-playbook fwbcld_app_create.yml -i hosts  -e 'ansible_python_interpreter=/usr/bin/python3'
   ```

**Example to configure OpenAPI Validation  in Fortinet's FortiWeb Cloud**

1. Create `fwbcld_openapi_validation.yml` with the following template:

   ```yaml
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
        application_name: "YOUR_APP_NAME"

      tasks:
        - name: Setup OpenApi Validation
          cloudwaf_openapi_validation:
            app_name: "{{application_name}}"
            enable: True
            action: "alert", "alert_deny", or "deny_no_log"
            validation_files:
              - /path/openapi_validation_file_1.yaml
              - /path/openapi_validation_file_2.yaml
   ```

2. Create the `hosts` inventory file:

   ```

    [fortiwebcloud]
    fortiwebcloud01 ansible_host="api.fortiweb-cloud.com" ansible_user="Your Account" ansible_password="Your Password"

    [fortiwebcloud:vars]
    ansible_network_os=fortinet.fortiwebcloud.fortiwebcloud
   ```

3. Run the test:

   ```bash
    ansible-playbook fwbcld_openapi_validation.yml -i hosts  -e 'ansible_python_interpreter=/usr/bin/python3'
   ```


## License

[License](https://github.com/fortinet/fortiwebcloud-ansible/blob/master/LICENSE)© Fortinet Technologies. All rights reserved.

## Support

Fortinet-provided scripts in this and other GitHub projects do not fall under the regular Fortinet technical support scope and are not supported by FortiCare Support Services. For direct issues, please refer to the [Issues](https://github.com/fortinet/fortiwebcloud-ansible/issues) tab of this GitHub project. For other questions related to this project, contact github@fortinet.com.
