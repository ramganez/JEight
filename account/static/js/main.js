
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