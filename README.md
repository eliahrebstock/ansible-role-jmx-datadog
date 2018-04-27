# Ansible Role JMX Datadog

Overview
--------
Ansible role to setup JMX credentials and to add Datadog java agent. 

Usage
-----

Add the role to your playbook :

```yaml
role: peopledoc.jmx-datadog
user: username
password: changeit
port: 7199
```

You may want to add the [Datadog Ansible Role](https://github.com/DataDog/ansible-datadog) too :

```yaml
role: Datadog.datadog
become: yes
datadog_api_key: "{{ vault_datadog_api_key }}"
datadog_agent_version: "1:6.1.4-1"
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


Team
----
[Tribe Java](https://github.com/peopledoc/tribe-java/blob/master/documentation/applications.md)


Contributing
------------
[CONTRIBUTING](https://github.com/peopledoc/tribe-java/blob/master/documentation/contribution.md)


Installing
----------

`ansible-galaxy`

License
-------
BSD
