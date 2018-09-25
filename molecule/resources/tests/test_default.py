import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_jenkins_slave_installed(host):
    """
    Unit test for the presence of installed Jenkins slave
    :param host: instance under test
    :return: None
    """
    with host.sudo():
        f = host.file('/home/jenkins/bin/swarm-client-3.3.jar')

        assert f.exists
        assert f.user == 'jenkins'
        assert f.group == 'jenkins'


def test_jenkins_slave_service_running(host):
    """
    Unit test for docker service running
    :param host: instance under test
    :return: None
    """

    cmd = host.run('sudo systemctl status jenkins-slave')
    assert 'active (running) ' in cmd.stdout
