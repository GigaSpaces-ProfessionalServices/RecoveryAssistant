#!/usr/bin/python3
# *-* coding: utf-8 *-*

"""
init.py: initialization script
"""

from scripts.setenvredolog import *
import subprocess
import re
import json
import pathlib
import socket
import threading
import multiprocessing


def module_install(_module_name):
    r = subprocess.run(
        "pip list".split(), 
        stdout=subprocess.PIPE).stdout.decode().lower()
    if not re.search(_module_name.lower(), r):
        subprocess.run([f'pip install {_module_name}'], shell=True)


def sync_resource(_server_index, _resource_index):
    hostname = SERVERS[_server_index]['host']
    username = SERVERS[_server_index]["username"]
    password = SERVERS[_server_index]["password"]
    resource_name = RESOURCES_LIST[_resource_index]["name"]
    resource_location = RESOURCES_LIST[_resource_index]["location"]
    local_path = str(pathlib.PurePath(resource_location).joinpath(resource_name)).replace('\\','\\\\')
    resourceNetDrive = str(pathlib.PurePath(resource_location).drive).replace(':','$')
    resourceNetPath = f"{resourceNetDrive}{resource_location}".replace(pathlib.PurePath(resource_location).drive, '')
    remote_path = f"\\{SERVERS[_server_index]['host']}\{resourceNetPath}".replace('\\','\\\\')
    net_use_cmd = f"net use \\\\{hostname}\\{resourceNetDrive} {password} /USER:{username}"
    map_netpath_cmd = f"if not exist \\\\{hostname}\\{resourceNetDrive} ({net_use_cmd})"
    subprocess.run(map_netpath_cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    create_target_cmd = f'if not exist "\\\\{hostname}\\{resourceNetPath}" (md "{remote_path}")'
    subprocess.run(create_target_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    copy_files_cmd = f'copy "{local_path}" "{remote_path}" /Y'
    subprocess.run(copy_files_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def connect_server(_index):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 135
    a_socket.settimeout(3)
    check_port = a_socket.connect_ex((SERVERS[_index]['host'], port))
    a_socket.settimeout(None)
    if check_port == 0:
        sync_threads = [
            threading.Thread (target=sync_resource, args=(_index, r,), daemon=True) 
            for r in range(len(RESOURCES_LIST))
            ]
        for t in sync_threads:
            t.start()
        for t in sync_threads:
            t.join()
        # remove all mapped network paths
        _delete_netpath_cmd = f"net use * /DELETE /Y"
        subprocess.run(_delete_netpath_cmd, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    else:
        print("FAILED")




if __name__ == '__main__':
    # list of required python modules 
    modules = ['pyyaml','colorama','pyfiglet']
    # install required python modules
    processes = [
        multiprocessing.Process(target=module_install, args=(module,), daemon=True) 
        for module in modules
    ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    
    if SYNC_RESOURCES:
        global SERVERS, RESOURCES_LIST
        RESOURCES_LIST = [
            {"name": "redolog-client-1.0-SNAPSHOT-jar-with-dependencies.jar", "location": str(resourceLocation)},
            {"name": "sqlite3.exe", "location": str(resourceLocation)},
            {"name": "psexec.exe", "location": str(resourceLocation)},
            {"name": "spaceHosts.txt", "location": str(scriptLocation)}
            ]
        with open(pathlib.PurePath.joinpath(scriptLocation, spaceHostsFileName), 'r', encoding='utf-8') as jhf:
            SERVERS = json.load(jhf)
        
        connection_threads = [
            threading.Thread (target=connect_server, args=(i,), daemon=True) 
                for i in range(len(SERVERS))
                ]
        for t in connection_threads:
            t.start()
        for t in connection_threads:
            t.join()
