import mailbox
import base64
import hashlib
from pathlib import Path
from email.utils import parsedate
from datetime import datetime


done = set()
counter = 1
mb = mailbox.mbox('my_mbox_file.mbox', create=False)
for msg in mb:
  for part in msg.walk():
    if not part.get_content_type().startswith('image/'):
      continue
    print(part.get_filename(), part.get_content_type())
    date = parsedate(msg.get('Date'))
    date = datetime(*date[:7])
    payload = base64.b64decode(part.get_payload())
    key = hashlib.sha256(payload).digest()
    if key in done:
      print('Skipping - already done!')
      continue
    done.add(key)
    fnam = Path(date.isoformat() + '_' + part.get_filename())
    if Path('images').joinpath(fnam).exists():
      clash_counter = 1
      while Path('images').joinpath(fnam.stem + '_' + str(clash_counter) + fnam.suffix).exists():
        clash_counter += 1
      fnam = fnam.stem + '_' + str(clash_counter) + fnam.suffix
    Path('images').joinpath(fnam).write_bytes(payload)
    counter += 1
