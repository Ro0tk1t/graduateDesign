$("a[name='buy_or_del']").click(function(){
    var selected = {};
    $(".custom-control-input").each(function(){
        if(this.checked)
            selected[$(this).parent().attr("id")] = parseInt($(this).parent().next().next().next().text());
    });
    if($(this).attr("id") == "buy"){
        const url = '/home/pay/' + JSON.stringify(selected);
        $.get(url);
    }
    else if($(this).attr("id") == "del"){
        const url = '/home/delete/' + JSON.stringify(selected);
        $.get(url);
    }
});