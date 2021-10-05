$('button[id|=edit_material')
.click(
     function (event)
     {
       var index = $(this).attr('id').replace(/edit_material-/, '');
       $('#material_id').attr('value',index);
       $('#update_material_name').attr('value',$('table#mydatatable tbody #' + index +' .name').text());
       $('#update_material_price').attr('value',$('table#mydatatable tbody #' + index +' .price').text().split(" ")[0]);
       $('#update_material_margin').attr('value',$('table#mydatatable tbody #' + index +' .margin').text().split(" ")[0]);
       //console.log($('table#mydatatable tbody #' + index +' .units').text());
       $('select#update_material_units option').each(function(i, obj) {
         //console.log($(obj).text());
          if($(obj).text()==$('table#mydatatable tbody #' + index +' .units').text()){
            $(obj).attr('selected',true);
          }else{
            $(obj).attr('selected',false);
          }
        });


      }
);
