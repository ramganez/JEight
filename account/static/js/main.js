
$(document).ready(function(){

    // your javascript here

    $(".checkAll").change(function() {
        var toggled = $(this).val();
        toggleBox(toggled, this.checked);
        completeBtnActive();

    });


});



function toggleBox(toggled, checked) {
    var objList = document.getElementsByName(toggled)

    for(i = 0; i < objList.length; i++)
        objList[i].checked = checked;

}

function isOneChecked() {
    return ($("[name=checkAll]:checked").length > 0);
}

function completeBtnActive(){

    if (isOneChecked()){
        $("#complete").attr('class', 'button button-primary btnnext');
        $("#complete").removeAttr('disabled');
    }

    else{
        $("#complete").attr('class', 'btnnext');
        $("#complete").attr('disabled', true);
    }

}

function appendchecklistResult(data_array, _id){

    if (data_array.length != 0){
        var rows = $('#'+_id).find('tr:not( :last-child)')
        total = 0
        rows.each(function( index, value ){
//            $(this).children().last().empty();
//            $(this).children().last().html(data_array[index]);
            $(this).children().last().find('input').prop('disabled', true);
            $(this).children().last().find('input').val(data_array[index])
            total += parseFloat(data_array[index])
        });
        // $('#'+_id).children().last().append('<td class="boldme">'+ total.toFixed(2) +'</td>')
        $('#'+_id).children().last().children().last().text(total.toFixed(2))
    }
}

function show_errors(_errors, _id, type){

    if (type === 'expense_inves'){
        $.each(_errors, function(i, each_error_field) {
            $('#'+_id+each_error_field).css("border-bottom-color", "red");
        });
    }

    if (type === 'afp'){
        $.each(_errors, function(i, each_error_field) {
            if($.isEmptyObject(each_error_field) !== true){
                $('#'+_id+i.toString()+"-amount").css("border-bottom-color", "red");
                }
        });
    }

    if (type === 'indiv'){
        $.each(_errors, function(i, each_error_field) {
            $('#'+_id+each_error_field).css("border-bottom-color", "red");
        });
    }
}

function enableChecklist(){
    console.log("inside checklist enableChecklist")
    // Enable submit icon
    $("#savechecklist").attr("onclick", "submitChecklist('paid_form');");

    $('.paid_display_off').find('input').removeAttr('disabled');
    $('.paid_header_display_off').show();
    $('.paid_display_off').show();
    $('.paid_total_display_off').show();
}

//submit checklist form
function submitChecklist(_id){
    console.log("inside submit checklist")
    $("#savechecklist").removeAttr('onclick');

    $.ajax({
        type: "POST",
        url: $('#'+_id).attr('action'),
        data: $('#'+_id).serialize(), // serializes the form's elements.
        success: function(data)
        {
            $('html, body').animate({
                scrollTop: $("#ResultStr").offset().top
            }, 2000);

            appendchecklistResult(data['expense'],'expense_table_body');
            appendchecklistResult(data['investment'],'inves_table_body');
            appendchecklistResult(data['afp'],'afp_table_body');
            appendchecklistResult(data['individual_share'],'monthshare_detail_table_body');

            console.log(data['result_str'])
            $('#ResultStr').text(data['result_str']);
            $('#get_checklist_url').val(data['get_checklist_url']);

        },

        error: function(data)
        {
            $("#savechecklist").attr("onclick", "submitChecklist('paid_form');");

            error_json = data.responseJSON
            console.log(error_json['monthinves']);
            console.log(error_json['monthexp']);

            if ( error_json['monthexp'] !== null && error_json['monthexp'].length != 0 ) {
//                show_exp_errors
                show_errors(error_json['monthexp'], "id_monthexp-", "expense_inves");
            }

            if ( error_json['monthinves'] !== null && error_json['monthinves'].length != 0 ) {
//                show_inves_errors
                show_errors(error_json['monthinves'], 'id_monthinves-', 'expense_inves');
            }

            if ( error_json['afp'] !== null && error_json['afp'].length != 0 ) {
//                show_inves_errors
                show_errors(error_json['afp'], 'id_adjustmentfrompeople_set-', 'afp');
            }

        }
    });
    return false;
}

function showHistoryWithChecklist(url_){

    $.ajax({
        type: "get",
        url: url_,
        dataType: "json",
        success: function(data){
            appendchecklistResult(data['expense'],'expense_table_body');
            appendchecklistResult(data['investment'],'inves_table_body');
            appendchecklistResult(data['afp'],'afp_table_body');
            appendchecklistResult(data['individual_share'],'monthshare_detail_table_body');

            $('.paid_header_display_off').show();
            $('.paid_display_off').show();
            $('.paid_total_display_off').show();

            $('#ResultStr').text(data['result_str']);
        },
        error: function(){
            // show original values
            $('.paid_header_display_off').show();
            $('.paid_display_off').show();
            $('.paid_total_display_off').show();
        }
    });

}
