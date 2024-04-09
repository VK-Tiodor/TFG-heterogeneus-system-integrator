import argparse
import os
import subprocess


def remove_images(project_dir):
    image_ids= subprocess.check_output(['docker', 'image', 'ls', '-aq'], cwd=project_dir)
    subprocess.run(['docker', 'rmi', *image_ids.split()], cwd=project_dir)


def remove_volumes(project_dir):
    volume_ids= subprocess.check_output(['docker', 'volume', 'ls', '-q'], cwd=project_dir)
    subprocess.run(['docker', 'volume', 'rm', *volume_ids.split()], cwd=project_dir)


parser = argparse.ArgumentParser(
    prog='Undeployer',
    description='Undeploys the heterogeneous system integrator. Default behaviour: Stops and removes the containers.'
)
parser.add_argument('-f', '--full', action='store_true', help='Removes everything')
parser.add_argument('-i', '--images', action='store_true', help='Removes also the images of the containers, for code updates')
parser.add_argument('-v', '--volumes', action='store_true', help='Removes also the volumes of the containers, for data flushing')
options = parser.parse_args()


project_dir = project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'heterogeneous_system_integrator')
subprocess.run(['docker', 'compose', 'down'], cwd=project_dir)
if options.full:
    remove_images(project_dir)
    remove_volumes(project_dir)
elif options.images:
    remove_images(project_dir)
elif options.volumes:
    remove_volumes(project_dir)
