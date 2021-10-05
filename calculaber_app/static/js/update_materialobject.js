/*$(window).load(function() {
   console.log("here");
   //Which will run only after page is fully loaded in background.
});*/

$(window).on('load', function() {
  $('table#object_detail_tbl > tbody  > tr').each(function(index, tr) {
     //console.log($(this).text());
     var price=Number($(this).find(".price").text().split(" ")[0]);
     var amount=Number($(this).find(".amount").text().split(" ")[0]);
     var margin=Number($(this).find(".margin").text().split(" ")[0]);
     $(this).find(".total").text(  Number(amount*(price*(1+(margin/100)))).toFixed(2) + " CZK");
     console.log(amount*(price*(1+(margin/100))));
  });
});

$('button[id|=edit_item')
.click(
     function (event)
     {
       var index = $(this).attr('id').replace(/edit_item-/, '');
       $('#materialobject_id').attr('value',index);

       $('#id_name_update').attr('value',$('table#object_detail_tbl tbody #' + index +' .name').text());

       $('#id_amount_update').attr('value',$('table#object_detail_tbl tbody #' + index +' .amount').text().split(" ")[0]);
       $('#id_price_update').attr('value',$('table#object_detail_tbl tbody #' + index +' .price').text().split(" ")[0]);
       $('#id_margin_update').attr('value',$('table#object_detail_tbl tbody #' + index +' .margin').text().split(" ")[0]);
       if($('table#object_detail_tbl tbody #' + index +' .amount').text().split(" ")[1]=="m2"){
         $('#amount_units').html('m<sup>2</sup>');
       }else{
         $('#amount_units').text($('#p_amount-' + index).text().split(" ")[1]);
       }

       if($('table#object_detail_tbl tbody #' + index).attr('class')=="customized"){
         $('#id_customized_update').prop('checked', true);
         $('.check_box_true').attr("hidden",false);
       }else{
         $('#id_customized_update').prop('checked', false);
         $('.check_box_true').attr("hidden",true);
       }

      }
);

$('#id_customized_update').click(function()
  {
    if($(this).prop("checked")==true){
      $('.check_box_true').attr("hidden",false);
    }else if($(this).prop("checked")==false){
      $('.check_box_true').attr("hidden",true);
    }
  }

);
