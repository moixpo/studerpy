# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Data included in the output binary
datas = [
    ("snowflake.jpg", "."),
    ("icone_albedo.ico", ".")
]

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
             hiddenimports=[],
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
