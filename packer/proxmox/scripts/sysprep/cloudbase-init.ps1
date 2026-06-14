# install Cloudbase-Init
mkdir "c:\setup"
echo "Copy CloudbaseInitSetup_Stable_x64.msi"
copy-item "G:\sysprep\CloudbaseInitSetup_Stable_x64.msi" "c:\setup\CloudbaseInitSetup_Stable_x64.msi" -force

echo "Start process CloudbaseInitSetup_Stable_x64.msi"
start-process -FilePath 'c:\setup\CloudbaseInitSetup_Stable_x64.msi' -ArgumentList '/qn /l*v C:\setup\cloud-init.log' -Wait

# Copy enable-winrm.ps1 to LocalScripts so Cloudbase-Init runs it on first boot of each clone.
# Cloudbase-Init's WinRMSetupPlugin handles the WinRM enable, but this script acts as
# belt-and-suspenders for GOAD's specific AllowUnencrypted/Basic auth requirements.
$localScripts = "C:\Program Files\Cloudbase Solutions\Cloudbase-Init\LocalScripts"
if (-not (Test-Path $localScripts)) { New-Item -ItemType Directory -Path $localScripts -Force | Out-Null }
copy-item "G:\enable-winrm.ps1" "$localScripts\enable-winrm.ps1" -force
