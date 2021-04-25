from dropbox import Dropbox
from pathlib import Path
import settings

db = Dropbox(settings.ACCESS_TOKEN)
folder = Path(settings.SRC_FOLDER)
for path in folder.glob("**/*"):
    if path.is_file() and not path.name.endswith(".part"):
        print(path.name)
        with open(path, "rb") as f:
            db.files_upload(f.read(), f"{settings.DST_FOLDER}{path.name}")
