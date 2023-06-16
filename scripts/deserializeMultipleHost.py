#!/usr/bin/python3
# *-* coding: utf-8 *-*

import subprocess
from setenvredolog import *

jarFilePath = str(jarFilePath).replace("\\","\\\\")
gsHome = str(gsHome).replace("\\","\\\\") + '\\\\'
resourceLocation = str(resourceLocation).replace("\\","\\\\") + '\\\\'
configLocation = str(configLocation).replace("\\","\\\\") + '\\\\'
targetPath = str(targetPath).replace("\\","\\\\") + '\\\\'
targetPathBaseDir = str(targetPathBaseDir).replace("\\","\\\\")
deserializeFullPath = str(deserializeFullPath).replace("\\","\\\\")

jCMD = f'java -jar "{jarFilePath}" RemoteDeserializeRedoLog \
--spaceName={spaceName} \
--gsHome="{gsHome} " \
--resourceLocation="{resourceLocation} " \
--configLocation="{configLocation} " \
--targetDir="{targetPath} " \
--targetPathBaseDir="{targetPathBaseDir} " \
--deserializeFullPath="{deserializeFullPath} "'


subprocess.run(jCMD, shell=True)

print()
subprocess.run('pause', shell=True)
