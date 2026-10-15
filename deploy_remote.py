"""
Automated Remote Deployment Script for Hetzner Server (89.167.22.10).
Uses Paramiko and SCP/SFTP to upload all project files and execute the build on Hetzner.
"""

import os
import sys
import time
from pathlib import Path
import paramiko

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent

# Server target
HETZNER_HOST = "89.167.22.10"
HETZNER_PORT = 22
HETZNER_USER = "root"
REMOTE_DIR = "/opt/mexconsumerpulse"

def deploy(password: str = None, key_path: str = None):
    print("=" * 65)
    print(f" Connecting to Hetzner server at {HETZNER_HOST}...")
    print("=" * 65)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if key_path and os.path.exists(key_path):
            print(f" -> Authenticating with SSH private key: {key_path}")
            try:
                k = paramiko.Ed25519Key.from_private_key_file(key_path)
            except Exception:
                try:
                    k = paramiko.RSAKey.from_private_key_file(key_path)
                except Exception:
                    k = None
            if k:
                ssh.connect(HETZNER_HOST, port=HETZNER_PORT, username=HETZNER_USER, pkey=k, timeout=10)
            else:
                ssh.connect(HETZNER_HOST, port=HETZNER_PORT, username=HETZNER_USER, key_filename=key_path, timeout=10)
        elif password:
            print(f" -> Authenticating with password: {'*' * len(password)}...")
            ssh.connect(HETZNER_HOST, port=HETZNER_PORT, username=HETZNER_USER, password=password, timeout=10)
        else:
            raise ValueError("No password or valid key_path provided.")

        print(" [SUCCESS] Connected to Hetzner server!")

        # 1. Ensure remote directory exists
        print(f" -> Preparing remote directory {REMOTE_DIR}...")
        ssh.exec_command(f"mkdir -p {REMOTE_DIR}/data {REMOTE_DIR}/reports {REMOTE_DIR}/frontend {REMOTE_DIR}/agents {REMOTE_DIR}/hetzner")

        # 2. Upload files via SFTP
        print(" -> Uploading application code and datasets via SFTP...")
        sftp = ssh.open_sftp()

        def upload_dir(local_path, remote_path):
            for item in os.listdir(local_path):
                if item in [".git", "__pycache__", ".venv", "venv", ".system_generated"]:
                    continue
                s_item = os.path.join(local_path, item)
                r_item = f"{remote_path}/{item}"
                if os.path.isdir(s_item):
                    try:
                        sftp.mkdir(r_item)
                    except IOError:
                        pass
                    upload_dir(s_item, r_item)
                else:
                    sftp.put(s_item, r_item)

        upload_dir(str(BASE_DIR), REMOTE_DIR)
        sftp.close()
        print(" [SUCCESS] All files uploaded to Hetzner!")

        # 3. Make deploy_hetzner.sh executable and run
        print("\n -> Executing deploy_hetzner.sh on Hetzner server...")
        stdin, stdout, stderr = ssh.exec_command(f"cd {REMOTE_DIR} && chmod +x deploy_hetzner.sh && ./deploy_hetzner.sh", get_pty=True)

        for line in iter(stdout.readline, ""):
            try:
                print(line, end="", flush=True)
            except UnicodeEncodeError:
                print(line.encode("ascii", errors="replace").decode("ascii"), end="", flush=True)

        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print("\n" + "=" * 65)
            print(f" 🎉 DEPLOYMENT COMPLETE! Access your site at: http://{HETZNER_HOST}:8080/")
            print("=" * 65)
        else:
            print(f"\n [ERROR] Deployment failed with exit code: {exit_status}")

    except Exception as e:
        print(f"\n [CONNECTION ERROR] Could not connect to {HETZNER_HOST}: {e}")
        return False
    finally:
        ssh.close()

    return True

if __name__ == "__main__":
    pwd = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else "@Wei2Shi4Lin2"
    key = sys.argv[2] if len(sys.argv) > 2 else None
    deploy(password=pwd, key_path=key)
