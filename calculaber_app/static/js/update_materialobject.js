$('button[id|=edit_item_test')
.click(
     function (event)
     {
       var index = $(this).attr('id').replace(/edit_item_test-/, '');
       $('#materialobject_id').attr('value',index)

       $('#text_name').attr('value',$('#p_name-' + index).text());

       $('#number_amount').attr('value',$('#p_amount-' + index).text().split(" ")[0]);
       $('#number_price').attr('value',$('#p_price-' + index).text().split(" ")[0])
       $('#number_margin').attr('value',$('#p_margin-' + index).text().split(" ")[0])

       if($('#customized-' + index).val()=="True"){
         $('#checkbox_customized').prop('checked', true);
         $('.check_box_true').attr("hidden",false);
       }
       else if($('#customized-' + index).val()=="False"){
         $('#checkbox_customized').prop('checked', false);
         $('.check_box_true').attr("hidden",true);
       }

      }
);

$('#checkbox_customized').click(function()
  {
    if($(this).prop("checked")==true){
      $('.check_box_true').attr("hidden",false);
    }
    else if($(this).prop("checked")==false){
      $('.check_box_true').attr("hidden",true);
    }
  }

);
