#!/usr/bin/python3
# *-* coding: utf-8 *-*

"""
recovery.py: main script
"""

if __name__ == '__main__':
    
    from scripts.setenvredolog import *
    from modules import (
        print_locations,
        print_header,
        pretty_print,
        press_any_key,
        validate_navigation_select,
        Spinner
    )
    import subprocess
    import os
    import yaml
    from platform import system
    
    spinner = Spinner
    initialization = str(raHome.joinpath('init.py'))
    print_header()
    with spinner('Initializing... ', delay=0.1):
        subprocess.run(initialization, shell=True)
    
    MENU_YAML = str(raHome.joinpath('config', 'menu.yaml'))
    user_selections = []
    
    def exec_target_ok(_target):
        """
        check target script
        :param target: a dictionary of available choices
        :return: True/False
        """
        # checking that target key is set
        if _target == '':
            _err_msg = f"CONFIG ERROR: missing 'target' value for '{_dict['id']}' option"
            pretty_print(_err_msg, 'red')
            return False
        # checking that target script exists
        _script = str(raHome.joinpath('scripts', _target))
        if not os.path.exists(_script):
            _err_msg = f"EXEC ERROR: target 'scripts/{os.path.basename(_script)}' not found"
            pretty_print(_err_msg, 'red')
            return False
        return True


    # load menu yaml
    with open(MENU_YAML, 'r', encoding="utf-8") as yml:
        data = yaml.safe_load(yml)
    try:
        while True:
            if len(user_selections) != 0:
                # building dynamic dictionary according to menu choices
                _dict = eval("data[" + ']['.join(user_selections) + "]",
                {"user_selections": user_selections, "data" : data})
            else:
                _dict = data
            print_locations(user_selections, data)
            if _dict['type'] == 'exec':
                # check target script
                if not exec_target_ok(_dict['target']):
                    press_any_key()
                    user_selections.pop()
                    continue
                # execute target script
                script = str(raHome.joinpath('scripts', _dict['target']))
                subprocess.call([script], shell=True)
                user_selections.pop()
                continue
            validate_navigation_select(_dict, user_selections)
    except (KeyboardInterrupt, SystemExit):
        if system() == 'Linux':
            os.system("stty sane ; stty erase ^H ; stty erase ^?")
        print('\nAborted!')
