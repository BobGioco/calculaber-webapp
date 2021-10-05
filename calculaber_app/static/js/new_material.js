$('button#new_material')
.click(
     function (event)
     {
       $('select#id_units option').each(function(i, obj) {
          if($(obj).text()=="m2"){
            $(obj).html('m<sup>2</sup>');
          }
        });
      }
);
