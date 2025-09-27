$(document).ready(function () {
    $('#example').DataTable();
});

function deleteTerm(designation){
    $.ajax("/term/" + designation, {
        type:"DELETE"
    })

}