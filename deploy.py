import argparse
import os
import subprocess


parser = argparse.ArgumentParser(
    prog='Deploye',
    description='Deploys the heterogeneous system integrator. Default behaviour: Creates and starts the containers.'
)
parser.add_argument('-b', '--build', help='Builds the heterogeneous system integrator image, for code updates.')
parser.add_argument('-d', '--detach', help='Starts the containers in "detach-mode", no logs available')
options = parser.parse_args()

project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'heterogeneous_system_integrator')
if options.build:
    subprocess.run(['docker', 'build', '-t', 'heterogeneous-system-integrator', '.'], cwd=project_dir)
command = 'docker compose up'
if options.detach:
    command = f'{command} -d'
subprocess.run(command.split(), cwd=project_dir)
