import subprocess
import os
import sys


project_dir = os.path.dirname(os.path.abspath(__file__))
subprocess.run(['docker', 'compose', 'down', '-v'], cwd=project_dir)
image_ids= subprocess.check_output(['docker', 'image', 'ls', '-aq'], cwd=project_dir)
subprocess.run(['docker', 'rmi', *image_ids.split()], cwd=project_dir)
