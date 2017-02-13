$(window).on('load', function() {
    var data_path = "../data/miserables.json";
    drawGraphFromJsonFile(data_path);

    $("#file_select_btn").on('click', function() {
        $("#file_select").click();
    });

    $("#file_select").on('change', function() {
        $("#file_name").text($('#file_select').val().split("\\").pop());
    });

    $('#upload_form').on('submit', function(evt){
        var formData = new FormData();
        formData.append("file", $('#file_select')[0].files[0]);
        $.ajax({
            url: $SCRIPT_ROOT + "_upload",
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function(data){
                drawGraph(JSON.parse(data));
            },
            error: function(err){
                console.log(err);
            }
        });
        return false;
    });
});
