$('button[id|=edit_item_test')
.click(
     function (event)
     {
       var index = $(this).attr('id').replace(/edit_item_test-/, '');
       $('#materialobject_id').attr('value',index);

       $('#id_name_update').attr('value',$('#p_name-' + index).text());

       $('#id_amount_update').attr('value',$('#p_amount-' + index).text().split(" ")[0]);
       $('#id_price_update').attr('value',$('#p_price-' + index).text().split(" ")[0]);
       $('#id_margin_update').attr('value',$('#p_margin-' + index).text().split(" ")[0]);
       if($('#p_amount-' + index).text().split(" ")[1]=="m2"){
         $('#amount_units').html('m<sup>2</sup>');
       }else{
         $('#amount_units').text($('#p_amount-' + index).text().split(" ")[1]);
       }

       if($('#customized-' + index).val()=="True"){
         $('#id_customized_update').prop('checked', true);
         $('.check_box_true').attr("hidden",false);
       }else if($('#customized-' + index).val()=="False"){
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
