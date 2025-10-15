import pytest


@pytest.mark.parametrize(
    "name",
    [
        "step-ca",
        "step-cli",
    ],
)
def test_packages(host, name):
    pkg = host.package(name)
    assert pkg.is_installed


def test_services(host):
    service = host.service("step-ca")
    assert service.is_running
    assert service.is_enabled


def test_tcp_sockets(host):
    socket = host.socket("tcp://127.0.0.1:443")
    assert socket.is_listening


def test_step_ca_config_name(host):
    assert host.file("/etc/step-ca/config/ca.json").contains("Example.com CA")


def test_step_ca_cert_subj(host):
    host_os = host.ansible("setup")["ansible_facts"]["ansible_os_family"]
    cmd = "openssl x509 -in /etc/step-ca/certs/root_ca.crt -noout -subject"

    if host_os == "RedHat":
        expected = "subject=O=Example.com CA, CN=Example.com CA Root CA"
    else:
        expected = "subject=O = Example.com CA, CN = Example.com CA Root CA"

    assert host.check_output(cmd) == expected


def test_step_ca_config_additional_fqdn(host):
    assert host.file("/etc/step-ca/config/ca.json").contains(
        '"alt-fqdn.local"',
    )
