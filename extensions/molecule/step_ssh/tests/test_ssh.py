from datetime import datetime

import pytest
import yaml


@pytest.fixture(scope="function")
def host_groups(host):
    return host.ansible.get_variables()["group_names"]


@pytest.fixture(scope="function", params=["ca_server", "ca_clients"])
def host_parameters(request):
    with open(f"tests/parameters/{request.param}.yml", "r") as f:
        try:
            return request.param, yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)


def test_host_files_exists(host, host_groups, host_parameters):
    group, params = host_parameters

    if group in host_groups:
        for i in params["files"]:
            assert host.file(i).exists


def test_host_services_running(host, host_groups, host_parameters):
    group, params = host_parameters

    if group in host_groups:
        for i in params["services"]:
            assert host.service(i).is_running
            assert host.service(i).is_running


def test_tls_duration(host, host_groups):
    if "ca_clients" in host_groups:
        hostname = host.ansible.get_variables()["inventory_hostname"]
        cmd = f"openssl x509 -in /etc/step/certs/{hostname}.crt -noout"
        date_format = "%b %d %H:%M:%S %Y %Z"

        start_date = host.run(cmd + " -startdate").stdout.split("=")[1]
        end_date = host.run(cmd + " -enddate").stdout.split("=")[1]

        start = datetime.strptime(start_date.strip(), date_format)
        end = datetime.strptime(end_date.strip(), date_format)
        delta = (end - start).days
        assert delta == 90


def test_ca_provisioners(host, host_groups):
    provisioners = ["JWK", "SSHPOP", "ACME"]

    if "ca_server" in host_groups:
        for i in provisioners:
            assert host.file("/etc/step-ca/config/ca.json").contains(i)
