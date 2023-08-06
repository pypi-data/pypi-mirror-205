from crosscompute.routines.asset import AssetStorage

from ..constants import PACKAGE_FOLDER


asset_storage = AssetStorage(PACKAGE_FOLDER / 'assets')


BARCODE_OUTPUT_HTML = asset_storage.load_string_text('barcode.html')
BARCODE_OUTPUT_JS = asset_storage.load_string_text('barcode-output.js')
