# Ansible Role JMX Datadog

![Build Status](https://travis-ci.org/peopledoc/ansible-role-jmx-datadog.svg?branch=master)

Overview
--------
Ansible role to setup JMX credentials and to add Datadog java agent.

Usage
-----

Add the role to your playbook :

```yaml
roles:
  - role: ansible-role-jmx-datadog
    vars:
      user: username
      password: changeit
      jmx_port: 7199
      jvm_user: user
      jvm_group: group
      jvm_user_id: 1000 # optional
      jvm_group_id: 1000 # optional
      app_instance_name: instance-name-on-datadog-interface

      datadog_api_key: "{{ vault_datadog_api_key }}"
      datadog_agent_version: "1:6.1.4-1"
      datadog_java_integration: yes
      datadog_config:
        tags: "env:{{ inventory_dir | basename }}"
        ...
```

`user` and `password` are the username/password pair for JMX (with readonly access).
They are mandatory and should be the same in the Datadog configuration.

`jvm_user` and `jvm_group` are the user/group who will run the application using JMX
(change access rights on default `jmxremote.password` and `jmxremote.access` files).

`jmx_port` is the port used by Datadog to contact the application using JMX on localhost.

If the ansible remote user is not `root` this role might fail. You can add
`become: true` to the role invocation in that case.

This role has the [Datadog Ansible Role](https://github.com/DataDog/ansible-datadog) as
a dependency and will configure the jmx check for it. You can add datadog role parameters
as parameters of this role (like `datadog_api_key`). You can also skip this role with
`--skip-tags datadog_agent`.

**You need to add `Datadog.datadog` to the requirements.yml of your project**. Cf [requirements.yml](requirements.yml).

If you want to install the Datadog agent but not the java integration from Datadog (for
example, if you want to use another java agent), you can disable it with
`datadog_java_integration: no`.

If you want to add more datadog checks configurations, you'll have to use the
`other_datadog_checks` variable as `datadog_checks` can't be override because
it is already in use as a role dependency parameter. The role will combine
`other_datadog_checks` and the check for jmx to obtain `datadog_checks`.

```yaml
roles:
  - role: ansible-role-jmx-datadog
    vars:
    ...
    other_datadog_checks:
      nginx:
        instances:
          ...

```

And the following JVM parameters :

```
-Dcom.sun.management.jmxremote.port=7199 -Dcom.sun.management.jmxremote.ssl=false
-javaagent:/usr/local/bin/dd-java-agent.jar -Ddd.service.name=instance-name-on-datadog-interface
```

This role doesn't setup SSL for JMX. You can safely disable it if the datadog
agent and the application using JMX are on the same host (the scenario assumed
by this role). If you setup the datadog agent on another host, you should setup SSL
for JMX using
[this documentation](https://docs.oracle.com/javase/1.5.0/docs/guide/management/agent.html#SSL_enabled)
and add configuration from [this documentation](https://docs.datadoghq.com/integrations/java/).

Tests
-----

Tests can be executed using:

`$ molecule --base-config molecule/base.yml test --driver-name docker --all`

The dependencies are ansible, molecule and docker Python packages.

License
-------
BSD
