import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_datadog_java_agent(host):
    assert not host.file("/usr/local/bin/dd-java-agent.jar").exists


def test_user_in_jmx_password(host):
    path = "/usr/lib/jvm/java-8-oracle/jre/lib/management/jmxremote.password"
    assert host.file(path).contains("jmxuser test123abc")


def test_user_in_jmx_access(host):
    path = "/usr/lib/jvm/java-8-oracle/jre/lib/management/jmxremote.access"
    assert host.file(path).contains("jmxuser readonly")


def test_datadog_agent_installed(host):
    assert host.exists("datadog-agent")
    cmd = host.run("datadog-agent version")
    assert cmd.rc == 0
    assert "Agent 6.1.4" in cmd.stdout


def test_datadog_yaml(host):
    path = "/etc/datadog-agent/datadog.yaml"
    ymlfile = host.file(path)
    assert ymlfile.exists
    assert ymlfile.contains("api_key: apikey")
    assert ymlfile.contains("tags: env:testing")


def test_datadog_jmx_yaml(host):
    path = "/etc/datadog-agent/conf.d/jmx.d/conf.yaml"
    ymlfile = host.file(path)
    assert ymlfile.exists


def test_datadog_test_yaml(host):
    path = "/etc/datadog-agent/conf.d/test.d/conf.yaml"
    ymlfile = host.file(path)
    assert ymlfile.exists
    assert ymlfile.contains("name: test")