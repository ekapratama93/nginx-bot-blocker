import os
import requests


download_url = "https://raw.githubusercontent.com/mitchellkrogza/nginx-ultimate-bad-bot-blocker/master/conf.d/globalblacklist.conf"
main_dir = os.getenv('MAIN_DIR', "./")
master_file = f'{main_dir}globalblacklist.conf'

r = requests.get(download_url)
with open(master_file, 'wb') as f:
    f.write(r.content)

output = open(f'{main_dir}bot-blocker.conf', 'w')
source = open(master_file, 'r')

allowed_bot = []
allowed_referer = []

with open(f'{main_dir}allowed-bot') as f:
    allowed_bot.extend(f.read().splitlines())

with open(f'{main_dir}allowed-referer') as f:
    allowed_referer.extend(f.read().splitlines())

lines = source.readlines()

for line in lines:
    normalized = line.strip()
    if normalized.startswith('#'):
        continue

    if not normalized:
        continue

    if "include" in normalized:
        continue

    if normalized.endswith('2;'):
        continue

    if "limit_conn_zone" in normalized:
        continue

    if "limit_req_zone" in normalized:
        continue

    if any(name in normalized for name in allowed_bot):
        continue

    if any(name in normalized for name in allowed_referer):
        continue

    output.write(line)

source.close()
output.close()

os.remove(master_file)
