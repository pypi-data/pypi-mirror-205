from crosscompute.routines.interface import (
    Batch)
from crosscompute.routines.variable import (
    Element,
    VariableView)

from ..constants import (
    BARCODE_JS_URI,
    FRAMES_PER_SECOND,
    SCANNER_HEIGHT_IN_PIXELS,
    SCANNER_WIDTH_IN_PIXELS)
from .asset import (
    BARCODE_OUTPUT_HTML,
    BARCODE_OUTPUT_JS)


class BarcodeView(VariableView):

    def render_output(self, b: Batch, x: Element):
        element_id = x.id
        variable_id = self.variable_id
        variable_definition = self.variable_definition
        c = b.get_variable_configuration(variable_definition)
        main_text = BARCODE_OUTPUT_HTML.substitute({
            'element_id': element_id,
            'mode_name': x.mode_name,
            'view_name': self.view_name,
            'variable_id': variable_id})
        js_texts = [
            BARCODE_OUTPUT_JS.substitute({
                'element_id': element_id,
                'frames_per_second': c.get(
                    'frames-per-second', FRAMES_PER_SECOND),
                'scanner_width_in_pixels': c.get(
                    'scanner-width-in-pixels', SCANNER_WIDTH_IN_PIXELS),
                'scanner_height_in_pixels': c.get(
                    'scanner-height-in-pixels', SCANNER_HEIGHT_IN_PIXELS)})]
        return {
            'css_uris': [], 'css_texts': [], 'js_uris': [BARCODE_JS_URI],
            'js_texts': js_texts, 'main_text': main_text}
