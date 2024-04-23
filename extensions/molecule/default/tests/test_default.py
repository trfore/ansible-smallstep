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
