import subprocess
import os

env = os.environ.copy()
env['SSH_ASKPASS'] = r'c:\Users\chris\Desktop\Market Research Mexico\hetzner\askpass.bat'
env['SSH_ASKPASS_REQUIRE'] = 'force'

# Update askpass.py to return @Wei2Shi4Lin2
with open(r'c:\Users\chris\Desktop\Market Research Mexico\hetzner\askpass.py', 'w', encoding='utf-8') as f:
    f.write('import sys\nprint("@Wei2Shi4Lin2")\n')

res = subprocess.run(
    ['ssh', '-o', 'StrictHostKeyChecking=no', '-o', 'PreferredAuthentications=password', 'root@89.167.22.10', 'echo', 'LOGIN_SUCCESS'],
    env=env,
    stdin=subprocess.DEVNULL,
    capture_output=True,
    text=True,
    timeout=15
)
print('STDOUT:', res.stdout)
print('STDERR:', res.stderr)
print('RC:', res.returncode)
