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
      jvm_user: user
      jvm_group: group
      jvm_user_id: 1000 # optional
      jvm_group_id: 1000 # optional
```

`user` and `password` are the username/password pair for JMX (with readonly access).
They are mandatory and should be the same in the Datadog configuration.

`jvm_user` and `jvm_group` are the user/group who will run the application using JMX
(change access rights on default `jmxremote.password` and `jmxremote.access` files).

You may want to add the [Datadog Ansible Role](https://github.com/DataDog/ansible-datadog) too :

```yaml
roles:
  - role: Datadog.datadog
    become: yes
    vars:
      datadog_api_key: "{{ vault_datadog_api_key }}"
      datadog_agent_version: "1:6.1.4-1"
      datadog_config:
        tags: "env:{{ inventory_dir | basename }}"
      datadog_checks:
        jmx:
          init_config:
          instances:
            - host: localhost
              port: 7199
              user: username
              password: changeit
              name: instance-name-on-datadog-interface
```

And the following JVM parameters :

```
-Dcom.sun.management.jmxremote.port=7199 -Dcom.sun.management.jmxremote.ssl=false
-javaagent:/usr/local/bin/dd-java-agent.jar -Ddd.service.name=instance-name-on-datadog-interface
```

Tests
-----

Tests can be executed using:

`$ molecule --debug test --driver-name docker`

The dependencies are ansible, molecule and docker-py Python packages.

License
-------
BSD
