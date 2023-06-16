#!/usr/bin/python3
# *-* coding: utf-8 *-*

import subprocess
import os
from setenvredolog import *

jarFilePath = str(jarFilePath).replace("\\","\\\\")
gsHome = str(gsHome).replace("\\","\\\\") + '\\\\'
resourceLocation = str(resourceLocation).replace("\\","\\\\") + '\\\\'
configLocation = str(configLocation).replace("\\","\\\\") + '\\\\'
targetPath = str(targetPath).replace("\\","\\\\") + '\\\\'
targetPathBaseDir = str(targetPathBaseDir).replace("\\","\\\\")
deserializeFullPath = str(deserializeFullPath).replace("\\","\\\\") + '\\\\'

jCMD = f'java -jar "{jarFilePath}" RemoteDownloadfiles \
--spaceName={spaceName} \
--gsHome="{gsHome} " \
--resourceLocation="{resourceLocation} " \
--configLocation="{configLocation} " \
--targetDir="{targetPath} " \
--targetPathBaseDir="{targetPathBaseDir} " \
--deserializeFullPath="{deserializeFullPath} "'

# create target folder if not exist
target_path = str(pathlib.PurePath(targetPathBaseDir).joinpath('AllDeserializedFiles'))
if not os.path.exists(target_path):
    os.makedirs(target_path)

subprocess.run(jCMD, shell=True)
print()
subprocess.call('pause', shell=True)
