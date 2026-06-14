"""
Unit tests for psmodules-airgap.zip integrity.
No live WinRM deps — safe for CI.
"""
import unittest
import zipfile
from pathlib import Path

SAGA_ROOT = Path(__file__).resolve().parents[1]
ZIP_PATH = SAGA_ROOT / "ansible" / "files" / "psmodules" / "psmodules-airgap.zip"

REQUIRED_MODULES = [
    "ComputerManagementDsc",
    "xNetworking",
    "xDnsServer",
    "ActiveDirectoryDsc",
]

MIN_SIZE_BYTES = 800_000  # zip must be >800KB (4 modules)


class TestAirgapZipExists(unittest.TestCase):
    def test_zip_exists(self):
        self.assertTrue(ZIP_PATH.exists(), f"psmodules-airgap.zip not found at {ZIP_PATH}")

    def test_zip_minimum_size(self):
        size = ZIP_PATH.stat().st_size
        self.assertGreater(
            size, MIN_SIZE_BYTES,
            f"zip too small ({size}B < {MIN_SIZE_BYTES}B) — likely missing modules"
        )

    def test_zip_is_valid(self):
        self.assertTrue(zipfile.is_zipfile(str(ZIP_PATH)), "zip file is corrupt/invalid")


class TestAirgapZipContents(unittest.TestCase):
    def setUp(self):
        self.zf = zipfile.ZipFile(str(ZIP_PATH))
        self.names = self.zf.namelist()

    def tearDown(self):
        self.zf.close()

    def test_all_required_modules_present(self):
        for mod in REQUIRED_MODULES:
            has = any(n.startswith(mod + "/") or n == mod for n in self.names)
            self.assertTrue(has, f"Module '{mod}' missing from psmodules-airgap.zip")

    def test_computer_management_dsc_has_psd1(self):
        has = any("ComputerManagementDsc" in n and n.endswith(".psd1") for n in self.names)
        self.assertTrue(has, "ComputerManagementDsc missing .psd1 manifest")

    def test_xnetworking_has_psd1(self):
        has = any("xNetworking" in n and n.endswith(".psd1") for n in self.names)
        self.assertTrue(has, "xNetworking missing .psd1 manifest")

    def test_xdnsserver_has_psd1(self):
        has = any("xDnsServer" in n and n.endswith(".psd1") for n in self.names)
        self.assertTrue(has, "xDnsServer missing .psd1 manifest")

    def test_activedirectorydsc_has_psd1(self):
        has = any("ActiveDirectoryDsc" in n and n.endswith(".psd1") for n in self.names)
        self.assertTrue(has, "ActiveDirectoryDsc missing .psd1 manifest")

    def test_no_nested_zip_inside(self):
        nested = [n for n in self.names if n.endswith(".zip")]
        self.assertEqual(nested, [], f"Nested zip found: {nested}")

    def test_module_count_at_least_four(self):
        top_level = {n.split("/")[0] for n in self.names if "/" in n}
        self.assertGreaterEqual(
            len(top_level), 4,
            f"Expected >=4 module dirs, got {len(top_level)}: {top_level}"
        )


class TestAnsibleRolesAirgapPattern(unittest.TestCase):
    """Verify the air-gapped copy+extract pattern is present in all relevant roles."""

    ROLES_DIR = SAGA_ROOT / "ansible" / "roles"

    def _role_tasks(self, role):
        p = self.ROLES_DIR / role / "tasks" / "main.yml"
        if not p.exists():
            self.skipTest(f"Role {role} not found")
        return p.read_text()

    def test_common_role_has_airgap_copy(self):
        content = self._role_tasks("common")
        self.assertIn("psmodules-airgap.zip", content,
                      "common role missing airgap zip copy task")

    def test_common_role_has_expand_archive(self):
        content = self._role_tasks("common")
        self.assertIn("Expand-Archive", content,
                      "common role missing Expand-Archive extract task")

    def test_domain_controller_role_has_airgap_copy(self):
        content = self._role_tasks("domain_controller")
        self.assertIn("psmodules-airgap.zip", content,
                      "domain_controller role missing airgap zip copy task")

    def test_domain_controller_role_no_acceptlicense(self):
        content = self._role_tasks("domain_controller")
        self.assertNotIn("-AcceptLicense", content,
                         "domain_controller role still uses -AcceptLicense (PSGet 1.x incompatible)")

    def test_child_domain_role_has_airgap_copy(self):
        content = self._role_tasks("child_domain")
        self.assertIn("psmodules-airgap.zip", content,
                      "child_domain role missing airgap zip copy task")

    def test_child_domain_role_no_acceptlicense(self):
        content = self._role_tasks("child_domain")
        self.assertNotIn("-AcceptLicense", content,
                         "child_domain role still uses -AcceptLicense (PSGet 1.x incompatible)")


if __name__ == "__main__":
    unittest.main()
