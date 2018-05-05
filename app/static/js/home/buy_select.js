$("#buy").click(function(){
    var ids = [];
    $(".custom-control-input").each(function(){
        if(this.checked)
        ids.push($(this).parent().attr("id"));
        });
    var url = '/home/pay/' + ids.toString();
    $.get(url);
});