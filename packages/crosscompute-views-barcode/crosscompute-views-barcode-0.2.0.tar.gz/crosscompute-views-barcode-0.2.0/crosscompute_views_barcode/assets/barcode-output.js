const $element_id = new Html5QrcodeScanner('$element_id', {
  fps: $frames_per_second, qrbox: {width: $scanner_width_in_pixels, height: $scanner_height_in_pixels}}, false);
$element_id.render(function (decodedText, decodedResult) {
  document.getElementById('$element_id').dispatchEvent(new CustomEvent('decoded', {detail: {text: decodedText, result: decodedResult}}));
  document.getElementById('$element_id-decoded').innerHTML = decodedText;
});
