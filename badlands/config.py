import os

BASE_FOLDER = "Prova riconoscimento Calanchi"

BANDS_FOLDER = os.path.join('Prova riconoscimento Calanchi', "Bande")

B02_FILE = os.path.join(BANDS_FOLDER, "T33TUH_20200823T100031_B02_10m.jp2")
B03_FILE = os.path.join(BANDS_FOLDER, "T33TUH_20200823T100031_B03_10m.jp2")
B04_FILE = os.path.join(BANDS_FOLDER, "T33TUH_20200823T100031_B04_10m.jp2")
B08_FILE = os.path.join(BANDS_FOLDER, "T33TUH_20200823T100031_B08_10m.jp2")

SHP_FILE = os.path.join(BASE_FOLDER, "GIS", "Calanchi_2020.shp")

FEATURES_FOLDER = 'features'