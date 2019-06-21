# -*- mode: python -*-
import os
import os.path
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules


for i, x in enumerate(sys.argv):
    if x == '--name':
        cmdline_name = sys.argv[i+1]
        break
else:
    raise Exception('no name')

PY36BINDIR =  os.environ.get('PY36BINDIR')
VESTX_ELECTRUM_VERSION =  os.environ.get('VESTX_ELECTRUM_VERSION')

hiddenimports = collect_submodules('trezorlib')
hiddenimports += collect_submodules('hideezlib')
hiddenimports += collect_submodules('safetlib')
hiddenimports += collect_submodules('btchip')
hiddenimports += collect_submodules('keepkeylib')
hiddenimports += collect_submodules('websocket')

# safetlib imports PyQt5.Qt.  We use a local updated copy of pinmatrix.py until they
# release a new version that includes https://github.com/archos-safe-t/python-safet/commit/b1eab3dba4c04fdfc1fcf17b66662c28c5f2380e
hiddenimports.remove('safetlib.qt.pinmatrix')

hiddenimports += [
    'electrum_vestx',
    'electrum_vestx.base_crash_reporter',
    'electrum_vestx.base_wizard',
    'electrum_vestx.plot',
    'electrum_vestx.qrscanner',
    'electrum_vestx.websockets',
    'electrum_vestx.gui.qt',
    'PyQt5.sip',
    'PyQt5.QtPrintSupport',  # needed by Revealer

    'electrum_vestx.plugins',

    'electrum_vestx.plugins.hw_wallet.qt',

    'electrum_vestx.plugins.audio_modem.qt',
    'electrum_vestx.plugins.cosigner_pool.qt',
    'electrum_vestx.plugins.digitalbitbox.qt',
    'electrum_vestx.plugins.email_requests.qt',
    'electrum_vestx.plugins.keepkey.qt',
    'electrum_vestx.plugins.revealer.qt',
    'electrum_vestx.plugins.labels.qt',
    'electrum_vestx.plugins.trezor.qt',
    'electrum_vestx.plugins.hideez.client',
    'electrum_vestx.plugins.hideez.qt',
    'electrum_vestx.plugins.safe_t.client',
    'electrum_vestx.plugins.safe_t.qt',
    'electrum_vestx.plugins.ledger.qt',
    'electrum_vestx.plugins.virtualkeyboard.qt',
]

datas = [
    ('electrum_vestx/*.json', 'electrum_vestx'),
    ('electrum_vestx/locale', 'electrum_vestx/locale'),
    ('electrum_vestx/wordlist', 'electrum_vestx/wordlist'),
    ('electrum_vestx/gui/icons', 'electrum_vestx/gui/icons'),
]

datas += collect_data_files('trezorlib')
datas += collect_data_files('hideezlib')
datas += collect_data_files('safetlib')
datas += collect_data_files('btchip')
datas += collect_data_files('keepkeylib')

# Add the QR Scanner helper app
datas += [('contrib/CalinsQRReader/build/Release/CalinsQRReader.app', './contrib/CalinsQRReader/build/Release/CalinsQRReader.app')]

# Add libusb so Trezor and Safe-T mini will work
binaries = [('../libusb-1.0.dylib', '.')]
binaries += [('../libsecp256k1.0.dylib', '.')]
binaries += [('/usr/local/lib/libgmp.10.dylib', '.')]

# https://github.com/pyinstaller/pyinstaller/wiki/Recipe-remove-tkinter-tcl
sys.modules['FixTk'] = None
excludes = ['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter']
excludes += [
    'PyQt5.QtBluetooth',
    'PyQt5.QtCLucene',
    'PyQt5.QtDBus',
    'PyQt5.Qt5CLucene',
    'PyQt5.QtDesigner',
    'PyQt5.QtDesignerComponents',
    'PyQt5.QtHelp',
    'PyQt5.QtLocation',
    'PyQt5.QtMultimedia',
    'PyQt5.QtMultimediaQuick_p',
    'PyQt5.QtMultimediaWidgets',
    'PyQt5.QtNetwork',
    'PyQt5.QtNetworkAuth',
    'PyQt5.QtNfc',
    'PyQt5.QtOpenGL',
    'PyQt5.QtPositioning',
    'PyQt5.QtQml',
    'PyQt5.QtQuick',
    'PyQt5.QtQuickParticles',
    'PyQt5.QtQuickWidgets',
    'PyQt5.QtSensors',
    'PyQt5.QtSerialPort',
    'PyQt5.QtSql',
    'PyQt5.Qt5Sql',
    'PyQt5.Qt5Svg',
    'PyQt5.QtTest',
    'PyQt5.QtWebChannel',
    'PyQt5.QtWebEngine',
    'PyQt5.QtWebEngineCore',
    'PyQt5.QtWebEngineWidgets',
    'PyQt5.QtWebKit',
    'PyQt5.QtWebKitWidgets',
    'PyQt5.QtWebSockets',
    'PyQt5.QtXml',
    'PyQt5.QtXmlPatterns',
    'PyQt5.QtWebProcess',
    'PyQt5.QtWinExtras',
]

a = Analysis(['electrum-vestx'],
             hiddenimports=hiddenimports,
             datas=datas,
             binaries=binaries,
             excludes=excludes,
             runtime_hooks=['pyi_runtimehook.py'])

# http://stackoverflow.com/questions/19055089/
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

pyz = PYZ(a.pure)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon='electrum_vestx/gui/icons/electrum-vestx.ico',
          name=os.path.join('build/electrum-vestx/electrum-vestx', cmdline_name))

# trezorctl separate bin
tctl_a = Analysis([os.path.join(PY36BINDIR, 'trezorctl')],
                  hiddenimports=['pkgutil'],
                  excludes=excludes,
                  runtime_hooks=['pyi_tctl_runtimehook.py'])

tctl_pyz = PYZ(tctl_a.pure)

tctl_exe = EXE(tctl_pyz,
           tctl_a.scripts,
           exclude_binaries=True,
           debug=False,
           strip=False,
           upx=False,
           console=True,
           name=os.path.join('build/electrum-vestx/electrum-vestx', 'trezorctl.bin'))

coll = COLLECT(exe, #tctl_exe,
               a.binaries,
               a.datas,
               strip=False,
               upx=False,
               name=os.path.join('dist', 'electrum-vestx'))

app = BUNDLE(coll,
             name=os.path.join('dist', 'Vestx Electrum.app'),
             appname="Vestx Electrum",
	         icon='electrum-vestx.icns',
             version=VESTX_ELECTRUM_VERSION)
