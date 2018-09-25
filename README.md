# ar_jenkins_slave

This role deploys a Jenkins Swarm Slave to a SystemD compliant Linux 
(RHEL/CentOS 7, Debian/Ubuntu, etc.) server or a
Windows10 Desktop or a Windows 2102R2+ Server

## Requirements

Assumes that Jenkins is already installed on a remote machine and has the swarm
plugin installed.  Update default/main.yml to align with your Jenkins install.

## Role Variables

All variables used in this role are defined in defaults/main.yml.  The variables
are grouped into sections, where the variables that are intended to be
frequently changed/overridden are defined first and variables that are less
likely to be changed are defined last.

You can override the variables in any standard Ansible-way (e.g. group_vars,
host_vars, playbook variables, command-line, etc.).

The variables we define in this role are:

### Platform Agnostic
|Variable|Required?|Default|Choices|Comments|
|:---|:---:|:---|:---|:---|
|jenkins_slave_jenkins_username|yes|jenkins| |username to use when connecting to the master CI server|
|jenkins_slave_jenkins_password|yes|password| |password of the username above to connect to the master CI server|
|jenkins_slave_jenkins_slave_name|yes|"{{inventory_hostname}}"| |the name of the slave|
|jenkins_slave_swarm_labels|yes|"{{inventory_hostname}}"| |label of the slave.  multiple labels supported via a space-delimited string (e.g., "foo bar baz")|
|jenkins_slave_jenkins_master|yes|http://host.domain:8080| |url and port of the master server|
|jenkins_slave_swarm_num_executors|yes|2| |number of executors the slave will support|
|jenkins_slave_jenkins_user|yes|jenkins| |username on the local box that will run the jenkins slave|
|jenkins_slave_jenkins_home|yes|<ul><li> Linux: /home/{{jenkins_slave_jenkins_user}}</li><li> Windows: "C:\\Users\\{{ jenkins_slave_jenkins_user }}"</li></ul>| |home directory of the local user|
|jenkins_slave_bin_dir|yes|<ul><li> Linux: "{{ jenkins_slave_jenkins_home }}/bin"</li><li> Windows: "{{ jenkins_slave_jenkins_home }}\\bin"</li></ul>| |directory where the slave binary is installed|str|
|jenkins_slave_workspace_dir|yes|<ul><li> Linux: "{{ jenkins_slave_jenkins_home }}/workspace"</li><li> Windows: "{{ jenkins_slave_jenkins_home }}\\workspace"</li></ul>| |directory where slave workspace is located|
|jenkins_slave_log_dir|yes|<ul><li> Linux: "{{ jenkins_slave_jenkins_home }}/log"</li><li> Windows: "{{ jenkins_slave_jenkins_home }}\\log"</li></ul>| |directory where the slave logs will be kept|
|jenkins_slave_jenkins_swarm_jar|yes|swarm-client-3.3.jar| |jenkins swarm client jar filename|
|jenkins_slave_jenkins_swarm_jar_url|yes|https://repo.jenkins-ci.org/releases/org/jenkins-ci/plugins/swarm-client/3.3/swarm-client-3.3.jar| |URL to download the client|

### Linux
|Variable|Required?|Default|Choices|Comments|
|:---|:---:|:---|:---|:---|
|jenkins_slave_service_restart|yes|'no'|<ul><li>no</li><li>on-success</li><li>on-failure</li><li>on-abnormal</li><li>on-watchdog</li><li>on-abort</li><li>always</li></ul>|the value of the SystemD `Restart=` directive|
|jenkins_slave_service_restart_seconds|yes|3| |the amount of time (in seconds) to wait for restart|

### Windows
|Variable|Required?|Default|Choices|Comments|
|:---|:---:|:---|:---|:---|
|jenkins_slave_win_swarm_batch_file|yes|swarm_start.bat| |The name of the Windows batch file that starts the slave|
|jenkins_slave_win_create_user|yes|true|<ul><li>false</li><li>true</li></ul>|Whether (`true`) or not (`false`) to create a local user to run the slave|
|jenkins_slave_win_user_password|yes|password| |The password of the local user|

## Dependencies

A list of other roles hosted on Galaxy should go here, plus any details in 
regards to parameters that may need to be set for other roles, or variables 
that are used from other roles.

|Role|Description|Version|Source|
|:---|:---|:---:|:---|
|ar_java_openjdk|Installs the OpenJDK java package|master|https://github.com/watsonb/ar_java_openjdk.git|
|ar_win_java|Installs current version of Java via Chocolatey|master|https://github.com/watsonb/ar_win_java.git|

## Example Playbook

Including an example of how to use your role (for instance, with variables
passed in as parameters) is always nice for users too:

```yaml
- name: PLAY | (1) Role with defaults
  hosts: servers
  roles:
    - role: ar_jenkins_slave
```

```yaml
- name: PLAY | (2) Role with overrides
  hosts: servers
  roles:
    - role: ar_jenkins_slave
      jenkins_slave_jenkins_master: "https://jenkins.example.com/"
      jenkins_slave_jenkins_username: "jenkins"
      jenkins_slave_jenkins_password: "mypassword"
      jenkins_slave_swarm_labels: "{{ inventory_hostname }} molecule testing foo bar baz"
      jenkins_slave_jenkins_user: jenkins
      jenkins_slave_jenkins_swarm_jar: swarm-client-3.3.jar
      jenkins_slave_jenkins_swarm_jar_url: https://repo.jenkins-ci.org/releases/org/jenkins-ci/plugins/swarm-client/3.3/swarm-client-3.3.jar
      jenkins_slave_jenkins_home: "C:\\Users\\{{ jenkins_slave_jenkins_user }}"
      jenkins_slave_bin_dir: "{{ jenkins_slave_jenkins_home }}\\bin"
      jenkins_slave_workspace_dir: "{{ jenkins_slave_jenkins_home }}\\workspace"
      jenkins_slave_log_dir: "{{ jenkins_slave_jenkins_home }}\\log"
      jenkins_slave_win_user_password: ap@sswordthatm33tsWindowsRequ!rements?
      jenkins_slave_win_create_user: true
```

## License

TBD

## Author Information

|Author|E-mail|
|---|---|
|Ben Watson| |

## Role Development Information

### Testing
See [molecule/README.md](molecule/README.md)

### Contributing

1. Fork it
1. Create your feature branch (`git checkout -b my-new-feature`)
1. Commit your changes (`git commit -am 'Add some feature'`)
1. Push to the branch (`git push origin my-new-feature`)
1. Create new Pull Request

### Git SCM
Please refer to the .gitignore file and update accordingly depending on your
development environment, etc.  The particular file was generated at 
[gitignore.io](https://www.gitignore.io/) and contains settings for the following:
  - Ansible
  - Python
  - Vim
  - Eclipse
  - IntelliJ IDEA
  - Linux
  - Windows
  
### Versioning
Please update [VERSION.md](./VERSION.md) as you release new versions of your role and try to
abide by [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

### Self-contained
Please try to keep this role as self-contained as possible such that it may be
simply installed (e.g. `ansible-galaxy install`) and applied as part of a 
playbook.
