
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
    var rows = $('#'+_id).find('tr:not( :last-child)')
    total = 0
    rows.each(function( index, value ){
        $(this).children().last().empty();
        $(this).children().last().html(data_array[index]);
        total += parseInt(data_array[index])
    });
    $('#'+_id).children().last().append('<td class="boldme">'+ total +'</td>')
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
            $('.paid_display_off').show();
        },
        error: function()
        {
           alert("Error"); // show the response
        }
    });
}