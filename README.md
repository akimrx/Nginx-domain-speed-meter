# Domains Speed meter for Nginx or Apache

Collect data of send/receive speed to all domains at host.

## Install

* Create log format

Insert in nginx.conf

```
log_format  test '$host $bytes_sent $request_length $msec';
access_log /var/log/nginx/access_test.log test;
```
I'm use this in OpenVZ host and not use access_log in other `server` configurations

* Add User parameters to zabbix-agent.conf

```
UserParameter=domain-discovery,sudo $zabbix_config_dir/script/domain_monitor.py list None
UserParameter=domain[*],sudo $zabbix_config_dir/script/domain_monitor.py $1 $2
```

To work sudo i'm added 2 lines to sudoers

```
visudo
Defaults:zabbix !requiretty
zabbix ALL= (ALL) NOPASSWD: $zabbix_config_dir/script/domain_monitor.py, $zabbix_config_dir/script/getDomains.py
```

* Copy scripts files at folder $zabbix_config_dir/script

* Change settings in settings.py

* Import template to zabbix

* Add template to host.