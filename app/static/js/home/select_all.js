$(function(){
    $("#select_all").click(function(){
        var status = this.checked;
        var all = 0.0;
        $(".custom-control-input").each(function(){
            this.checked=status;
            all += parseFloat($(this).parent().next().next().text());
        });

        var amount_element = $("#sum");
        if(!status){
            amount_element.text(0);
        }
        else{
            amount_element.text(all);
        }
    });

    $(".custom-control-input").click(function(){
        var amount_element = $("#sum");
        var this_element = $(this);
        const amount = parseFloat(amount_element.text());
        if(this.checked){
            var price = parseFloat(this_element.parent().next().next().text());
            amount_element.text(price + amount);
        }
        else{
            var price = parseFloat(this_element.parent().next().next().text());
            amount_element.text(amount - price);
            }
    });
});
//input[name=box]