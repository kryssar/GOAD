#!/usr/bin/env python3
"""
Post-deploy live validation for SAGA Star Wars AD lab.
Runs read-only WinRM checks across all 5 VMs and exits non-zero on any failure.

Usage:
  python3 validate-post-deploy.py
  python3 validate-post-deploy.py --json
"""
import argparse
import json
import sys
import warnings
from datetime import datetime, timezone

warnings.filterwarnings("ignore")

try:
    import winrm
except ImportError:
    print("ERROR: pywinrm not installed. Use bridge-venv.")
    sys.exit(1)

HOSTS = [
    {"name": "dc01", "alias": "CORUSCANT-DC",    "ip": "10.10.20.10", "role": "galactic_empire_dc"},
    {"name": "dc02", "alias": "DS-COMMAND-DC",   "ip": "10.10.20.11", "role": "deathstar_dc"},
    {"name": "dc03", "alias": "ALDERAAN-DC",     "ip": "10.10.20.12", "role": "rebel_alliance_dc"},
    {"name": "srv02", "alias": "DS-WEAPONS-SRV", "ip": "10.10.20.22", "role": "member_server"},
    {"name": "srv03", "alias": "ALDERAAN-CA-SRV","ip": "10.10.20.23", "role": "member_server"},
]

REQUIRED_MODULES = ["ComputerManagementDsc", "xNetworking", "xDnsServer", "ActiveDirectoryDsc"]

PS_MODULES_CHECK = """
$req = @('ComputerManagementDsc','xNetworking','xDnsServer','ActiveDirectoryDsc')
$found = Get-Module -ListAvailable -Name $req | Select -ExpandProperty Name | Sort -Unique
$missing = $req | Where { $found -notcontains $_ }
if ($missing.Count -eq 0) { "ALL_PRESENT" } else { "MISSING:" + ($missing -join ',') }
"""

PS_DOMAIN_CHECK = """
try {
    $d = Get-ADDomain -ErrorAction Stop
    $u = (Get-ADUser -Filter * -ErrorAction Stop).Count
    "$($d.DNSRoot)|$u"
} catch {
    # Fallback for member servers without AD module
    $dom = (Get-WmiObject Win32_ComputerSystem).Domain
    if ($dom -and $dom -ne 'WORKGROUP') { "member:$dom" }
    else { "ERROR:$_" }
}
"""

PS_TRUST_CHECK = """
try {
    $trusts = Get-ADTrust -Filter * -ErrorAction Stop
    if ($trusts) { ($trusts | ForEach { "$($_.Name):$($_.Direction)" }) -join ',' }
    else { "NONE" }
} catch { "ERROR:$_" }
"""


def _session(ip):
    return winrm.Session(ip, auth=("vagrant", "vagrant"), transport="ntlm",
                         server_cert_validation="ignore")


def _run(sess, ps):
    r = sess.run_ps(ps)
    return r.std_out.decode().strip(), r.std_err.decode().strip()


def check_host(h):
    result = {"host": h["name"], "alias": h["alias"], "ip": h["ip"],
              "role": h["role"], "checks": {}, "pass": True, "errors": []}
    try:
        sess = _session(h["ip"])

        # WinRM reachability
        out, _ = _run(sess, "hostname")
        result["checks"]["winrm"] = {"ok": bool(out), "value": out}
        if not out:
            result["pass"] = False
            result["errors"].append("WinRM: empty hostname response")

        # PS modules
        out, _ = _run(sess, PS_MODULES_CHECK)
        ok = out == "ALL_PRESENT"
        result["checks"]["psmodules"] = {"ok": ok, "value": out}
        if not ok:
            result["pass"] = False
            result["errors"].append(f"PSModules: {out}")

        # Domain membership
        out, _ = _run(sess, PS_DOMAIN_CHECK)
        ok = not out.startswith("ERROR")
        result["checks"]["domain"] = {"ok": ok, "value": out}
        if not ok:
            result["pass"] = False
            result["errors"].append(f"Domain: {out}")

        # Trusts (DC only)
        if "dc" in h["name"]:
            out, _ = _run(sess, PS_TRUST_CHECK)
            ok = not out.startswith("ERROR")
            result["checks"]["trusts"] = {"ok": ok, "value": out}
            if not ok:
                result["pass"] = False
                result["errors"].append(f"Trusts: {out}")

    except Exception as e:
        result["pass"] = False
        result["errors"].append(f"Connection failed: {e}")
        result["checks"]["winrm"] = {"ok": False, "value": str(e)}

    return result


def validate_cross_domain(results):
    """After per-host checks, cross-check expected domain/trust topology."""
    findings = []

    # galactic.empire (dc01) must trust rebel.alliance bidirectionally
    dc01 = next((r for r in results if r["host"] == "dc01"), None)
    if dc01 and dc01["checks"].get("trusts", {}).get("ok"):
        trust_val = dc01["checks"]["trusts"]["value"]
        if "rebel.alliance" not in trust_val:
            findings.append("FAIL: galactic.empire has no trust to rebel.alliance")
        elif "bidirectional" not in trust_val.lower() and ":3" not in trust_val:
            findings.append(f"WARN: trust direction not Bidirectional: {trust_val}")

    # deathstar.galactic.empire (dc02) must be child domain
    dc02 = next((r for r in results if r["host"] == "dc02"), None)
    if dc02 and dc02["checks"].get("domain", {}).get("ok"):
        domain_val = dc02["checks"]["domain"]["value"]
        if "deathstar.galactic.empire" not in domain_val:
            findings.append(f"FAIL: dc02 not in deathstar.galactic.empire: {domain_val}")

    # rebel.alliance (dc03)
    dc03 = next((r for r in results if r["host"] == "dc03"), None)
    if dc03 and dc03["checks"].get("domain", {}).get("ok"):
        domain_val = dc03["checks"]["domain"]["value"]
        if "rebel.alliance" not in domain_val:
            findings.append(f"FAIL: dc03 not in rebel.alliance: {domain_val}")

    return findings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results = []
    for h in HOSTS:
        if not args.json:
            print(f"  checking {h['name']:6s} ({h['ip']}) ... ", end="", flush=True)
        r = check_host(h)
        results.append(r)
        if not args.json:
            status = "PASS" if r["pass"] else "FAIL"
            print(status)
            for e in r["errors"]:
                print(f"           ! {e}")

    cross = validate_cross_domain(results)
    failed_hosts = [r for r in results if not r["pass"]]
    all_pass = len(failed_hosts) == 0 and len(cross) == 0

    if not args.json:
        print()
        if cross:
            for c in cross:
                print(f"  TOPOLOGY: {c}")
        print(f"\n{'PASS' if all_pass else 'FAIL'} — {len(results) - len(failed_hosts)}/{len(results)} hosts OK"
              f"{', ' + str(len(cross)) + ' topology errors' if cross else ''}")
    else:
        print(json.dumps({
            "ts": datetime.now(timezone.utc).isoformat(),
            "pass": all_pass,
            "hosts_ok": len(results) - len(failed_hosts),
            "hosts_total": len(results),
            "topology_errors": cross,
            "results": results,
        }, indent=2))

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
