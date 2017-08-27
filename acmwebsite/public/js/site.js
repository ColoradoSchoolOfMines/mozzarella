$(document).ready(function() {
    function change_theme(theme_name) {
        $('#bs-css').attr('href', '/css/bootstrap.' + theme_name + '.min.css');
        $('#toggle-theme').text('Too ' + theme_name + '?');
    }

    $('#toggle-theme').click(function (event) {
        event.preventDefault();
        $.get("/toggle_theme", change_theme, "text");
    });

    $(".vupdate").on("change keyup paste", function() {
        $(this).attr("value", $(this).val());
    });

    $('input[name="first_time"]').change(function() {
        checked = this.checked;
        $('.on_first_time').each(function() {
            if (checked) { $(this).fadeIn() } else { $(this).fadeOut() }
        });
    });
});
