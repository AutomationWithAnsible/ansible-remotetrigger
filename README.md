Jenkins Remote Deploy Role 
=========
This role triggers build on jenkins machine

```
jenkins_remotedeploy_url                :  "http://localhost:8080"
jenkins_remotedeploy_job                :  "test-remote_trigger"
jenkins_remotedeploy_force              :  false
jenkins_remotedeploy_first_boot_file    :  "/var/local/jenkins_first_boot_file"
jenkins_remotedeploy_parameters         :
                                          - python_path :  "/opt/bin/"
                                          - foo         : "parm" 
```

## Contributors
* [Adham Helal](https://github.com/ahelal)
