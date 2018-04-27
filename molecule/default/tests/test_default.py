import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_datadog_java_agent(host):
    assert host.file("/usr/local/bin/dd-java-agent.jar").exists


def test_user_in_jmx_password(host):
    path = "/usr/lib/jvm/java-8-oracle/jre/lib/management/jmxremote.password"
    assert host.file(path).contains("jmxuser test123abc")


def test_user_in_jmx_access(host):
    path = "/usr/lib/jvm/java-8-oracle/jre/lib/management/jmxremote.access"
    assert host.file(path).contains("jmxuser readonly")
