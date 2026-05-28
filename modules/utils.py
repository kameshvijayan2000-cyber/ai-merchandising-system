import json
import os
import shutil
from datetime import datetime

# ================= LOAD JSON =================
def load_json(path):

    if os.path.exists(path):

        try:

            with open(path, "r") as f:

                return json.load(f)

        except:

            return {}

    return {}

# ================= SAVE JSON =================
def save_json(path, data):

    # CREATE FOLDER
    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    # SAVE FILE
    with open(path, "w") as f:

        json.dump(
            data,
            f,
            indent=4
        )

    # ================= AUTO BACKUP =================
    os.makedirs(
        "backup",
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = os.path.basename(path)

    backup_path = os.path.join(
        "backup",
        f"{timestamp}_{filename}"
    )

    shutil.copy(path, backup_path)

# ================= CLEAR ALL =================
def clear_all_data():

    files = [

        "data/style_master.json",
        "data/fabric_program.json",
        "data/count_data.json",
        "data/fabric_store.json",
        "data/production_tracking.json"

    ]

    for file in files:

        with open(file, "w") as f:

            json.dump({}, f)