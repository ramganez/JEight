
$(document).ready(function(){

    // your javascript here
    $(".checkAll").change(function() {
        var toggled = $(this).val();
        toggleBox(toggled, this.checked);
    });

});


function toggleBox(toggled, checked) {
    var objList = document.getElementsByName(toggled)

    for(i = 0; i < objList.length; i++)
        objList[i].checked = checked;
}
