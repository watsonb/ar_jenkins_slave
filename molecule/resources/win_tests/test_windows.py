import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_default(host):
    """
    Default unit test that always passes
    :param host: instance under test
    :return: None
    """
    assert 1 == 1


def test_temp_directory_exits(host):
    """
    Unit test for the presence of the Windows temp directory
    :param host: instance under test
    :return: None
    """

    assert host.ansible(
        "win_file",
        "path='C:\\temp' state=directory"
        )["changed"] is False


def test_jenkins_slave_running(host):
    """
    Unit test for the presence of jenkins slave service running
    :param host: instance under test
    :return: None
    """

    cmd = host.ansible(
        "win_shell",
        "executable=cmd nssm status jenkins-slave",
        check=False
        )["stdout"]

    assert "SERVICE_RUNNING" in cmd
