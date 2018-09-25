#jinja2:newline_sequence:'\r\n'
rem {{ansible_managed}}

cd {{ jenkins_slave_bin_dir }}
"java" -jar {{ jenkins_slave_jenkins_swarm_jar }} -username {{ jenkins_slave_jenkins_username }} -password {{ jenkins_slave_jenkins_password }} -name {{ jenkins_slave_jenkins_slave_name }} -labels "{{ jenkins_slave_swarm_labels }}" -master {{ jenkins_slave_jenkins_master }} -fsroot {{ jenkins_slave_workspace_dir }} -retry 5 -mode exclusive -executors {{ jenkins_slave_swarm_num_executors }} -disableSslVerification
