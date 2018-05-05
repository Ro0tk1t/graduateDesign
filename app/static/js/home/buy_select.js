$("#buy").click(function(){
    var ids = {};
    $(".custom-control-input").each(function(){
        if(this.checked)
            ids[$(this).parent().attr("id")] = parseInt($(this).parent().next().next().next().text());
        });
    var url = '/home/pay/' + JSON.stringify(ids);
    $.get(url);
});