import subprocess
import paramiko
from functions import script



def is_docker_installed():
    script.info_msg("Checking if Docker is installed...")

    try:
        subprocess.check_output(["docker", "--version"])
        docker_installed = True
    except subprocess.CalledProcessError:
        docker_installed = False

    if docker_installed == True:
        script.info_msg("Docker is installed.\n\n")
        return True
    else:
        script.info_msg("Docker is not installed.\n\n")

        return False



def is_podman_installed():
    script.info_msg("Checking if Podman is installed...")
    try:
        subprocess.check_output(["podman", "--version"])
        podman_installed = True
    except (FileNotFoundError, subprocess.CalledProcessError):
        podman_installed = False

    if podman_installed == True:
        script.info_msg("Podman is installed.\n\n")
        return True
    else:
        script.info_msg("Podman is not installed.\n\n")
        return False



def kill_and_delete_docker_containers():
    script.info_msg("Attempting to kill and remove all Docker containers...")

    ls_cont_cmd = "docker ps -aq"   
    container_ids = subprocess.check_output(ls_cont_cmd, shell=True).decode().strip().split('\n')

    if len(container_ids) == 1: 
        script.ok_msg("No containers to stop and remove.\n\n")
    else:  
        for container_id in container_ids:
            stop_cmd = f"docker stop {container_id}"
            subprocess.run(stop_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            remove_cmd = f"docker rm -f {container_id}"
            subprocess.run(remove_cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            print(f"Container {container_id} stopped and removed.") # Cant easily implement ok_msg here...
        print("\n\n")




def kill_and_delete_podman_containers():
    script.info_msg("Attempting to kill and remove all Podman containers...")

    subprocess.run('podman kill -a', shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run('podman rm -f -a', shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    script.ok_msg("Containers stopped and removed.\n\n")








