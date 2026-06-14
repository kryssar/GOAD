"dc01" = {
  name               = "CORUSCANT-DC"
  desc               = "CORUSCANT-DC - galactic.empire - WinServer2019 - {{ip_range}}.10"
  cores              = 2
  memory             = 3096
  clone              = "WinServer2019_x64"
  dns                = "{{ip_range}}.1"
  ip                 = "{{ip_range}}.10/24"
  gateway            = "{{ip_range}}.1"
}
"dc02" = {
  name               = "DS-COMMAND-DC"
  desc               = "DS-COMMAND-DC - deathstar.galactic.empire - WinServer2019 - {{ip_range}}.11"
  cores              = 2
  memory             = 3096
  clone              = "WinServer2019_x64"
  dns                = "{{ip_range}}.1"
  ip                 = "{{ip_range}}.11/24"
  gateway            = "{{ip_range}}.1"
}
"dc03" = {
  name               = "ALDERAAN-DC"
  desc               = "ALDERAAN-DC - rebel.alliance - WinServer2016 - {{ip_range}}.12"
  cores              = 2
  memory             = 3096
  clone              = "WinServer2016_x64"
  dns                = "{{ip_range}}.1"
  ip                 = "{{ip_range}}.12/24"
  gateway            = "{{ip_range}}.1"
}
"srv02" = {
  name               = "DS-WEAPONS-SRV"
  desc               = "DS-WEAPONS-SRV - deathstar.galactic.empire - WinServer2019 - {{ip_range}}.22"
  cores              = 2
  memory             = 6240
  clone              = "WinServer2019_x64"
  dns                = "{{ip_range}}.1"
  ip                 = "{{ip_range}}.22/24"
  gateway            = "{{ip_range}}.1"
}
"srv03" = {
  name               = "ALDERAAN-CA-SRV"
  desc               = "ALDERAAN-CA-SRV - rebel.alliance - WinServer2016 - {{ip_range}}.23"
  cores              = 2
  memory             = 5120
  clone              = "WinServer2016_x64"
  dns                = "{{ip_range}}.1"
  ip                 = "{{ip_range}}.23/24"
  gateway            = "{{ip_range}}.1"
}