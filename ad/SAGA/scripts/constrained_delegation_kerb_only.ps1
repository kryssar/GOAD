# https://www.thehacker.recipes/ad/movement/kerberos/delegations/constrained#without-protocol-transition
Set-ADComputer -Identity "ds-weapons-srv$" -ServicePrincipalNames @{Add='HTTP/ds-command-dc.deathstar.galactic.empire'}
Set-ADComputer -Identity "ds-weapons-srv$" -Add @{'msDS-AllowedToDelegateTo'=@('HTTP/ds-command-dc.deathstar.galactic.empire','HTTP/ds-command-dc')}
# Set-ADComputer -Identity "ds-weapons-srv$" -Add @{'msDS-AllowedToDelegateTo'=@('CIFS/ds-command-dc.deathstar.galactic.empire','CIFS/ds-command-dc')}