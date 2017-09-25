(function($) {
  // Copy the schedule URL to the clipboard.
  // https://stackoverflow.com/a/30810322/2319844
  $('#copy-link').on('click', function() {
    $('#schedule-url').select();
    document.execCommand('copy');
  });
})(jQuery);
