(function($){
    var last_query = "";
    $("#ml-username").on("change keyup paste", function(){
        if ($("#ml-username").val().indexOf("@") >= 0) {
            $("#ml-username").val($("#ml-username").val().replace(/\@.*$/g, ""));
            alert("Only a Mines username is required, not a full email address.");
        }
        if ($("#ml-username").val() != last_query && $("#ml-username").val().length > 1) {
            last_query = $("#ml-username").val();
            $.getJSON("https://mastergo.mines.edu/mpapi/uid/" + encodeURIComponent($("#ml-username").val()), function(data) {
                if (data["result"] == "success") {
                    $("#ml-fullname").val(data["attributes"]["first"] + " " + data["attributes"]["sn"]);
                    $(".ml-fullname-warn").fadeIn();
                }
                else {
                    $("#ml-fullname").val("");
                    $(".ml-fullname-warn").fadeOut();
                }
            });
        }
    });

    $('#mailinglist-form').submit(function() {
        $(this).find("button[type='submit']").prop('disabled',true);
    });

})(jQuery);
