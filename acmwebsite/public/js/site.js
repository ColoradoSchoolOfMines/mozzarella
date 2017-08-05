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
});
