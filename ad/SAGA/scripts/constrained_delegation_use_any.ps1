Set-ADUser -Identity "darth.revan" -ServicePrincipalNames @{Add='CIFS/starforge.deathstar.galactic.empire'}
Get-ADUser -Identity "darth.revan" | Set-ADAccountControl -TrustedToAuthForDelegation $true
Set-ADUser -Identity "darth.revan" -Add @{'msDS-AllowedToDelegateTo'=@('CIFS/ds-command-dc.deathstar.galactic.empire','CIFS/ds-command-dc')}