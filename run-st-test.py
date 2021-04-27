import subprocess
import os, sys
import streamlit as st

config_name = 'st-run-test.py'

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    running_mode = 'Frozen/executable'
else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive (e.g. 'python myapp.py')"
        print(running_mode)
    except NameError:
        application_path = os.getcwd()
        running_mode = 'Interactive'

config_full_path = os.path.join(application_path, config_name)
print(config_full_path)

# logging.debug('CWD: ' + os.getcwd())

cmd = "/Users/xingchen/anaconda3/envs/comp_soc_sci_2021/bin/streamlit"
cmd_args = "run"
cmd_args2 = "st-run-test.py"
subprocess.run([cmd, cmd_args, config_full_path])
