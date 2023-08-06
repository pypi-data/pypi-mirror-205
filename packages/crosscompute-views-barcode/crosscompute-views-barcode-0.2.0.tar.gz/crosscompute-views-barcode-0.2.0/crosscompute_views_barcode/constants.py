from pathlib import Path


PACKAGE_FOLDER = Path(__file__).parent
ASSETS_FOLDER = PACKAGE_FOLDER / 'assets'


BARCODE_JS_URI = 'https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js'
FRAMES_PER_SECOND = 10
SCANNER_WIDTH_IN_PIXELS = 256
SCANNER_HEIGHT_IN_PIXELS = 256
