#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, Adham Helal <adham.helal@yetu.com>
#
# This file is part of Ansible.
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

__author__ = 'Adham Helal'

DOCUMENTATION = '''
---
module: jenkins_trigger
short_description: Trigger a job in jenkins with/without parameters
version_added: "0.1.0"
description:
            - Trigger a job in jenkins.
            - Optionally send a dictionary parameters
            - Optionally do authentication
options:
    name:
        description:
          - Jenkins job name
        required: true
    url:
        description:
          - Jenkins job url
        required: true
    parm:
        description:
            - A dictionary of parameters to inject in job
notes:
   - Will always return changed if job exists, else will fail
   - Supports basic authentication
requirements: [ jenkinsapi ]
'''

EXAMPLES = '''
- name: Trigger a job no parm
  jenkins_trigger:
     name="test-remote_trigger"
     url="jenkins.example.com:8080"
- name: Trigger a job with parm
  jenkins_trigger:
     name="test-remote_trigger"
     url="jenkins.example.com:8080"
  args:
    parm:
        x: 1
        y: 2
        z: 3
- name: Trigger a job auth
  jenkins_trigger:
     name="test-remote_trigger"
     url="jenkins.example.com:8080"
     user=foo
     password=pass
'''


class JenkinTrigger():
    def __init__(self, module):
        self.module = module
        self.job_name = self.module.params['name']
        self.jenkins_url = self.module.params['url']
        self.jenkins_parm = self.module.params['parm']
        self.jenkins_user = self.module.params['user']
        self.jenkins_password = self.module.params['password']

    def main(self):
        try:
            J = Jenkins(self.jenkins_url, username=self.jenkins_user, password=self.jenkins_password)
        except Exception, e:
            self.module.fail_json(msg="Jenkins connection to '{}' Issue: ".format(self.jenkins_url, e.message))

        try:
            J.build_job(self.job_name, self.jenkins_parm)
        except jenkinsapi.custom_exceptions.WillNotBuild:
            self.module.exit_json(changed=False, msg="Job is already triggered.", job_name=self.job_name,
                                  jenkins_url=self.jenkins_url)
        except jenkinsapi.custom_exceptions.UnknownJob:
            self.module.fail_json(msg="Job '{}' does not exist on '{}'".format(self.job_name, self.jenkins_url))

        self.module.exit_json(changed=True, msg="Job triggered.", job_name=self.job_name, jenkins_url=self.jenkins_url)


        self.module.exit_json(changed=True, msg="Job triggered.", job_name=self.job_name, jenkins_url=self.jenkins_url)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(default=None, required=True),
            user=dict(default=None, required=False),
            password=dict(default=None, required=False),
            url=dict(default=None, required=True),
            parm=dict(default=None, type="dict")
        ),
        # No need to support check mode
        supports_check_mode=False
    )
    JenkinTrigger(module).main()
    if not jenkinsapi_client_found:
        module.fail_json(msg="The Jenkins Trigger module requires jenkinsapi library. use 'pip install jenkinsapi' ")

try:
    from jenkinsapi.jenkins import Jenkins
    import jenkinsapi
except ImportError:
    jenkinsapi_client_found = False
else:
    jenkinsapi_client_found = True

# import module snippets
from ansible.module_utils.basic import *
main()
