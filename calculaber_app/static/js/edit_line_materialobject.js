$('button[id|=edit_item')
.click(
     function (event)
     {
       var index = $(this).attr('id').replace(/edit_item-/, '');
       $('#pk-' + index).attr('value',index)

       $('#p_name-' + index).hide();
       $('#input_name-' + index).show();
       $('#input_name-' + index).attr('value',$('#p_name-' + index).text());

       $('#p_amount-' + index).hide();
       $('#input_amount-' + index).show();
       $('#input_amount-' + index).attr('value',$('#p_amount-' + index).text());

       $('#close_item-' + index).show();
       $('#delete_item-' + index).hide();
       $('#edit_item-' + index).hide();
       $('#done-' + index).show();

       $('button[id|=edit_item').prop("disabled",true);
       $('input[id|=delete_item').attr('disabled','true');
     }
);

$('button[id|=close_item')
.click(
     function (event)
     {
       var index = $(this).attr('id').replace(/close_item-/, '');
       $('#pk-' + index).attr('value',"")

       $('#p_name-' + index).show();
       $('#input_name-' + index).val('');
       $('#input_name-' + index).hide();

       $('#p_amount-' + index).show();
       $('#input_amount-' + index).hide();
       $('#input_amount-' + index).val('');

       $('#close_item-' + index).hide();
       $('#delete_item-' + index).show();
       $('#edit_item-' + index).show();
       $('#done-' + index).hide();

       $('button[id|=edit_item').prop("disabled",false);
       $('input[id|=delete_item').removeAttr('disabled');
     }
);
