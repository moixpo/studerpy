# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

DEBUG = True

# Data included in the output binary
media_dir = "media"
additional_directories = ["csvExport", "FigureExport"]

datas = [
    (os.path.join(media_dir, direntry.name), media_dir)
    for direntry in os.scandir(media_dir)
]
datas.extend((dir, dir) for dir in additional_directories)

print(datas)


def add_optional_dataframes():
    def _():
        optional_data = (
            "saved_dataframe_log_day",
            "saved_dataframe_log_min",
            "saved_dataframe_log_month",
            "saved_dataframe_log_quarters",
            "saved_dataframe_log_year",
        )
        for dataframe_file in optional_data:
            if os.path.exists(dataframe_file):
                yield (dataframe_file, ".")
    return list(_())


datas.extend(add_optional_dataframes())

a = Analysis(['tkinter_GUI_datalogviewer.py'],
             #pathex=['C:\\Users\\b\\tkinterdatalogviewer\\Studer Datalog Viewer'],
             binaries=[],
             datas=datas,
             hiddenimports=["tkcalendar", "babel.numbers"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='tkinter_GUI_datalogviewer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='tkinter_GUI_datalogviewer')
