"""Run with python3 -m unittest discover -s tests (no router required)."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


INIT = Path(__file__).resolve().parents[1] / "openwrt-bandix/files/bandix.init"


class HostArgumentsTest(unittest.TestCase):
    def start_service(self, host=None, modern=True, iface="br-lan", excluded="", arp_resolve=False, traffic=True, neighbor_resolve=None):
        with tempfile.TemporaryDirectory() as directory:
            binary = Path(directory) / "bandix"
            binary.write_text("#!/bin/sh\nprintf '%s\\n' '" + ("--host --geoip-dir --traffic-exclude-ips --traffic-neighbor-resolve" if modern else "--port --traffic-arp-resolve") + "'\n")
            binary.chmod(0o755)
            script = r'''
. "$TEST_INIT"
PROG="$TEST_BINARY"
config_load() { :; }
config_get() {
    local value="$4"
    case "$3" in
        iface) value="$TEST_IFACE" ;;
        traffic_exclude_ips) value="$TEST_EXCLUDED" ;;
        traffic_neighbor_resolve) value="${TEST_NEIGHBOR_RESOLVE-}" ;;
        port) value=8686 ;;
        data_dir) value=/tmp/bandix-test-data ;;
        host) value="${TEST_HOST-$4}" ;;
    esac
    eval "$1=\$value"
}
config_get_bool() {
    local value=0
    case "$2.$3" in
        traffic.enabled) value="$TEST_TRAFFIC_ENABLED" ;;
        connections.enabled) value="$TEST_CONNECTIONS_ENABLED" ;;
        traffic.traffic_arp_resolve) value="$TEST_ARP_RESOLVE" ;;
        traffic.traffic_neighbor_resolve) value="${TEST_NEIGHBOR_RESOLVE:-0}" ;;
    esac
    eval "$1=\$value"
}
procd_open_instance() { :; }
procd_set_param() {
    [ "$1" = command ] || return 0
    shift
    printf '%s\n' "$@"
}
procd_append_param() { shift; printf '%s\n' "$@"; }
procd_close_instance() { :; }
logger() { printf '%s\n' "$*" >&2; }
start_service
'''
            env = dict(os.environ, TEST_INIT=str(INIT), TEST_BINARY=str(binary),
                       TEST_IFACE=iface, TEST_EXCLUDED=excluded,
                       TEST_ARP_RESOLVE="1" if arp_resolve else "0",
                       TEST_TRAFFIC_ENABLED="1" if traffic else "0",
                       TEST_CONNECTIONS_ENABLED="0" if traffic else "1")
            env.pop("TEST_NEIGHBOR_RESOLVE", None)
            if neighbor_resolve is not None:
                env["TEST_NEIGHBOR_RESOLVE"] = "1" if neighbor_resolve else "0"
            env.pop("TEST_HOST", None)
            if host is not None:
                env["TEST_HOST"] = host
            return subprocess.run(["sh", "-c", script], env=env, text=True, capture_output=True)

    def test_default_and_empty_configs_pass_loopback(self):
        for host in [None, ""]:
            with self.subTest(host=host):
                result = self.start_service(host)
                self.assertEqual(result.returncode, 0, result.stderr)
                args = result.stdout.splitlines()
                self.assertEqual(args[args.index("--host") + 1], "127.0.0.1")

    def test_custom_ipv4_and_ipv6_remain_single_arguments(self):
        for host in ["0.0.0.0", "192.168.2.1", "::", "::1", "fd00::1"]:
            with self.subTest(host=host):
                result = self.start_service(host)
                self.assertEqual(result.returncode, 0, result.stderr)
                args = result.stdout.splitlines()
                self.assertEqual(args[args.index("--host") + 1], host)
                self.assertIn("--enable-traffic", args)
                self.assertIn("--geoip-dir", args)

    def test_excluded_addresses_become_one_argument(self):
        result = self.start_service(excluded="192.168.1.2 fd00::2")
        self.assertEqual(result.returncode, 0, result.stderr)
        args = result.stdout.splitlines()
        self.assertEqual(args.count("--traffic-exclude-ips"), 1)
        self.assertEqual(args[args.index("--traffic-exclude-ips") + 1], "192.168.1.2,fd00::2")
        self.assertEqual(args[args.index("--iface") + 1], "br-lan")

    def test_legacy_binary_rejects_exclusions_before_starting(self):
        result = self.start_service(modern=False, excluded="192.168.1.2")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("does not support IP exclusion", result.stderr)

    def test_neighbor_resolution_is_opt_in_and_requires_traffic(self):
        for enabled, traffic, expected in [(False, True, False), (True, True, True), (True, False, False)]:
            with self.subTest(enabled=enabled, traffic=traffic):
                result = self.start_service(neighbor_resolve=enabled, traffic=traffic)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual("--traffic-neighbor-resolve" in result.stdout.splitlines(), expected)

    def test_legacy_binary_rejects_neighbor_resolution_before_starting(self):
        result = self.start_service(modern=False, neighbor_resolve=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("does not support active neighbor resolution", result.stderr)

    def test_legacy_arp_setting_is_used_only_when_new_setting_is_missing(self):
        for current, expected in [(None, True), (False, False), (True, True)]:
            with self.subTest(current=current):
                result = self.start_service(arp_resolve=True, neighbor_resolve=current)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual("--traffic-neighbor-resolve" in result.stdout.splitlines(), expected)
                self.assertNotIn("--traffic-arp-resolve", result.stdout.splitlines())

    def test_legacy_binary_keeps_working_with_default_config(self):
        result = self.start_service(modern=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("--host", result.stdout.splitlines())
        self.assertNotIn("--traffic-exclude-ips", result.stdout)

    def test_legacy_binary_rejects_unsupported_custom_bind_before_starting(self):
        result = self.start_service("0.0.0.0", modern=False)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("does not support --host", result.stderr)


if __name__ == "__main__":
    unittest.main()
