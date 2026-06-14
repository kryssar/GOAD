Install-WindowsFeature -Name GPMC
$gpo_exist = Get-GPO -Name "RepublicWallpaper" -erroraction ignore

if ($gpo_exist) {
    # Do nothing
    #Remove-GPO -Name "RepublicWallpaper"
    #Remove the link of the GPO Remove-RepublicWallpaper if it exists
    #Remove-GPLink -Name "RepublicWallpaper" -Target "DC=deathstar,DC=galactic,DC=empire" -erroraction 'silentlycontinue'
} else {
    New-GPO -Name "RepublicWallpaper" -comment "Change Wallpaper"
    New-GPLink -Name "RepublicWallpaper" -Target "DC=deathstar,DC=galactic,DC=empire"

    #https://www.thewindowsclub.com/set-desktop-wallpaper-using-group-policy-and-registry-editor
    Set-GPRegistryValue -Name "RepublicWallpaper" -key "HKEY_CURRENT_USER\Control Panel\Colors" -ValueName Background -Type String -Value "100 175 200"
    #Set-GPPrefRegistryValue -Name "RepublicWallpaper" -Context User -Action Create -Key "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System" -ValueName Wallpaper -Type String -Value "C:\tmp\GOAD.png"

    Set-GPRegistryValue -Name "RepublicWallpaper" -key "HKEY_CURRENT_USER\Control Panel\Desktop" -ValueName Wallpaper -Type String -Value ""
    #Set-GPPrefRegistryValue -Name "RepublicWallpaper" -Context User -Action Create -Key "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System" -ValueName WallpaperStyle -Type String -Value "4"

    Set-GPRegistryValue -Name "RepublicWallpaper" -Key "HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows NT\CurrentVersion\WinLogon" -ValueName SyncForegroundPolicy -Type DWORD -Value 1

    # Allow darth.malak to Edit Settings of the GPO
    # https://learn.microsoft.com/en-us/powershell/module/grouppolicy/set-gppermission?view=windowsserver2022-ps
    Set-GPPermissions -Name "RepublicWallpaper" -PermissionLevel GpoEditDeleteModifySecurity -TargetName "darth.malak" -TargetType "User"
}