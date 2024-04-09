import subprocess
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
subprocess.run(['docker', 'build', '-t', 'heterogeneous-system-integrator', '.'], cwd=project_dir)
subprocess.run(['docker', 'compose', 'up', '-d'], cwd=project_dir)
