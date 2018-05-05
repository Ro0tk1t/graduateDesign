$(function(){
    $("#select_all").click(function(){
        var status = this.checked;
        var all = 0.0;
        $(".custom-control-input").each(function(){
            this.checked=status;
            var price_element = $(this).parent().next().next();
            all += parseFloat(price_element.text()) * parseFloat(price_element.next().text());
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
        var price_element = $(this).parent().next().next();
        const amount = parseFloat(amount_element.text());
        var price = parseFloat(price_element.text()) * parseFloat(price_element.next().text());
        if(this.checked){
            amount_element.text(amount + price);
        }
        else{
            amount_element.text(amount - price);
            }
    });
});
//input[name=box]