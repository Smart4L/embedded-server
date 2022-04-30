
import subprocess
output = subprocess.getoutput("ifconfig wwan0 | egrep -o 'inet [0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}'  | cut -d' ' -f2")
if output.startswith("169."):
  print("CA MARCHE PAS")
else:
  print("LET GO")