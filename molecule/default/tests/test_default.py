import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_datadog_java_agent(host):
    assert host.file("/usr/local/bin/dd-java-agent.jar").exists


def test_user_in_jmx_password(host):
    java_home = host.run(". /etc/profile && echo $JAVA_HOME").stdout
    path = java_home + "/jre/lib/management/jmxremote.password"
    jmx_file = host.file(path)
    assert jmx_file.exists
    assert jmx_file.contains("jmxuser test123abc")
    if jmx_file.is_symlink:
        real_jmx_file = host.file(jmx_file.linked_to)
        assert real_jmx_file.user == "testuser"
        assert real_jmx_file.group == "testuser"
        assert real_jmx_file.mode == 0o600
    elif jmx_file.is_file:
        assert jmx_file.user == "testuser"
        assert jmx_file.group == "testuser"
        assert jmx_file.mode == 0o600
    else:
        assert False


def test_user_in_jmx_access(host):
    java_home = host.run(". /etc/profile && echo $JAVA_HOME").stdout
    path = java_home + "/jre/lib/management/jmxremote.access"
    jmx_file = host.file(path)
    assert jmx_file.exists
    assert jmx_file.contains("jmxuser readonly")
    if jmx_file.is_symlink:
        real_jmx_file = host.file(jmx_file.linked_to)
        assert real_jmx_file.user == "testuser"
        assert real_jmx_file.group == "testuser"
    elif jmx_file.is_file:
        assert jmx_file.user == "testuser"
        assert jmx_file.group == "testuser"
    else:
        assert False


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
    assert ymlfile.contains("name: app-test-instance")
    assert ymlfile.contains("password: test123abc")
    assert ymlfile.contains("port: 7199")
    assert ymlfile.contains("user: jmxuser")


def test_datadog_test_yaml(host):
    path = "/etc/datadog-agent/conf.d/test.d/conf.yaml"
    ymlfile = host.file(path)
    assert ymlfile.exists
    assert ymlfile.contains("name: test")
