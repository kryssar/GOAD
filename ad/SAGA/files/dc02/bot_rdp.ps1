# https://learn.microsoft.com/fr-fr/troubleshoot/windows-server/user-profiles-and-logon/turn-on-automatic-logon
if(-not(query session mission.vao /server:ds-weapons-srv)) {
  #kill process if exist
  Get-Process mstsc -IncludeUserName | Where {$_.UserName -eq "DEATHSTAR\mission.vao"}|Stop-Process
  #run the command
  mstsc /v:ds-weapons-srv
}