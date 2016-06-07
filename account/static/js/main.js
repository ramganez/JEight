
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
            $(this).children().last().empty();
            $(this).children().last().html(data_array[index]);
            total += parseFloat(data_array[index])
        });
        $('#'+_id).children().last().append('<td class="boldme">'+ total.toFixed(2) +'</td>')
    }
}


function show_errors(_errors, _id){

    $.each(_errors, function(i, each_error_field) {
        $('#'+_id+each_error_field).css("border-bottom-color", "red");
    });

}


//submit checklist form
function submitChecklist(_id){
    $.ajax({
        type: "POST",
        url: $('#'+_id).attr('action'),
        data: $('#'+_id).serialize(), // serializes the form's elements.
        success: function(data)
        {
            $('.paid_display_off').hide();
            appendchecklistResult(data['expense'],'expense_table_body');
            appendchecklistResult(data['investment'],'inves_table_body');
            appendchecklistResult(data['afp'],'afp_table_body');
            appendchecklistResult(data['individual_share'],'monthshare_detail_table_body');
            $('.paid_display_off').show();
            console.log(data['result_str'])
            $('#ResultStr').text(data['result_str']);
        },
        error: function(data)
        {
            error_json = data.responseJSON
            console.log(error_json['monthinves']);
            console.log(error_json['monthexp']);

            if ( error_json['monthexp'] !== null && error_json['monthexp'].length != 0 ) {
//                show_exp_errors
                show_errors(error_json['monthexp'], "id_monthexp-");
            }

            if ( error_json['monthinves'] !== null && error_json['monthinves'].length != 0 ) {
//                show_inves_errors
                show_errors(error_json['monthinves'], 'id_monthinves-');
            }

        }
    });

    $('html, body').animate({
        scrollTop: $("#ResultStr").offset().top
    }, 2000);

}