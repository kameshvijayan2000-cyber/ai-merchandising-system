import os
import json
import shutil

DATA_FOLDER = "data"


# ================= CREATE DATA FOLDER =================
def ensure_data_folder():

    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)


# ================= LOAD JSON =================
def load_json(file_path):

    ensure_data_folder()

    if not os.path.exists(file_path):
        return {}

    try:
        with open(file_path, "r") as f:
            return json.load(f)

    except:
        return {}


# ================= SAVE JSON =================
def save_json(file_path, data):

    ensure_data_folder()

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


# ================= CLEAR ALL DATA =================
def clear_all_data():

    if os.path.exists(DATA_FOLDER):
        shutil.rmtree(DATA_FOLDER)

    os.makedirs(DATA_FOLDER)