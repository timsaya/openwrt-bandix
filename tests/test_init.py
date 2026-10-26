"""Run with python3 -m unittest discover -s tests (no router required)."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


INIT = Path(__file__).resolve().parents[1] / "openwrt-bandix/files/bandix.init"


class HostArgumentsTest(unittest.TestCase):
    def start_service(self, host=None, modern=True):
        with tempfile.TemporaryDirectory() as directory:
            binary = Path(directory) / "bandix"
            binary.write_text("#!/bin/sh\nprintf '%s\\n' '" + ("--host --geoip-dir" if modern else "--port") + "'\n")
            binary.chmod(0o755)
            script = r'''
. "$TEST_INIT"
PROG="$TEST_BINARY"
config_load() { :; }
config_get() {
    local value="$4"
    case "$3" in
        iface) value=br-lan ;;
        port) value=8686 ;;
        data_dir) value=/tmp/bandix-test-data ;;
        host) value="${TEST_HOST-$4}" ;;
    esac
    eval "$1=\$value"
}
config_get_bool() {
    local value=0
    [ "$2" = traffic ] && value=1
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
            env = dict(os.environ, TEST_INIT=str(INIT), TEST_BINARY=str(binary))
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

    def test_legacy_binary_keeps_working_with_default_config(self):
        result = self.start_service(modern=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("--host", result.stdout.splitlines())

    def test_legacy_binary_rejects_unsupported_custom_bind_before_starting(self):
        result = self.start_service("0.0.0.0", modern=False)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("does not support --host", result.stderr)


if __name__ == "__main__":
    unittest.main()
