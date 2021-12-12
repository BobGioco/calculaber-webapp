$(document).ready(function(){
  $("table").on("submit","form.delete_material",function(e){
    e.preventDefault();
    var item_id=$(this).closest('tr').attr("id");
    $.ajax({
      url:'',
      type:'post',
      data:{
        item_id: item_id,
        type:'delete',
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
      },
      dataType: 'json',
      error: function (request, error) {
        console.log(arguments);
        alert(" Can't do because: " + error);
      },
      success: function(response){
        response_data=response;
        material=material.filter(item => item.id!=item_id)
        var row = document.getElementById(item_id);
        row.parentNode.removeChild(row);
        console.log(response_data);
        console.log('done');
      }
    });
  });

  //$('button.update').click(function (event){
  $('table').on("click", "button.update", function (event){
        console.log('hi');
         var index = Number($(this).closest('tr').attr('id'));
         var temp_data=material.find(item => item.id === index);
         $('#material_id').attr('value',index);
         $('#update_material_name').val(temp_data['name']);
         $('#update_material_price').val(temp_data['price']);
         $('#update_material_margin').val(temp_data['margin']);
         $('form.update_material input#id_tag').val('');
         $('select#update_material_units option').each(function(i, obj) {
            if($(obj).attr('value')===temp_data['units']){
              $(obj).attr('selected',true);
            }else{
              $(obj).attr('selected',false);
            }
          });
        }
  );

  $("form.update_material").submit(function(e){
    e.preventDefault();
    $.ajax({
      url:'',
      type:'post',
      data:{
        item_id:$('#material_id').val(),
        name:$('#update_material_name').val(),
        price:$('#update_material_price').val(),
        margin:$('#update_material_margin').val(),
        units:$("#update_material_units").val(),
        tags:new_tag_array,
        type:'update',
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()},
      error: function (request, error) {
        console.log(arguments);
        alert(" Can't do because: " + error);
      },
      success: function(response){
        response_data=response;
        $('#' + response_data['id'] + " td.name").text(response_data['name']);
        $('#' + response_data['id'] + " td.price").text(FormatNumber(response_data['price']) + ' Kč');
        $('#' + response_data['id'] + " td.margin").text(FormatNumber(response_data['margin']) + ' %');
        $('#' + response_data['id'] + " td.units").text(choice_array[response_data['units']]);
        var tr='';
        tag_array=tag_array.filter(item => item.material_id != Number(response_data['id']));
        tr+="<div class='tag__popup'>";
        JSON.parse(response_data['tag_list']).forEach( x=>{
          console.log(x.tag);
          tag_array.push(x);
          tr+="<div class='tag-box'><p class='tag tag--flex'>" + x.tag + "</p></div>";
        });
        tr+="</div>";
        $('#' + response_data['id'] + " td.table-material__tags").html(tr);
        var to_update_data=material.findIndex(item => item.id === response_data['id']);
        material[to_update_data]=response_data;
        console.log($('#' + response_data['id'] + " td.name").text());
        console.log(response_data);
        console.log('done');
        $('#UpdateMaterial').modal('hide');
      }
    });
  });

  $("form.new_material").submit(function(e){
    e.preventDefault();
    $.ajax({
      url:'',
      type:'post',
      data:{
        name:$('#new_material_name').val(),
        price:$('#new_material_price').val(),
        margin:$('#new_material_margin').val(),
        units:$("#new_material_units").val(),
        tags:new_tag_array,
        type:'new',
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()},
      error: function (request, error) {
        console.log(arguments);
        alert(" Can't do because: " + error);
      },
      success: function(response){
        response_data=response;
        var table = document.getElementById("mydatatable").getElementsByTagName("tbody")[0];
        tr="";
        tr+="<tr class='table-material__data' id='" + response_data['id'] + "'>";
        tr+="<td class='table-material__item name'>"+response_data['name']+'</td>'+"<td class='table-material__margin margin'>"+FormatNumber(response_data['margin'])+' %</td>'+"<td class='table-material__price price'>"+FormatNumber(response_data['price'])+' Kč</td>'+"<td class='table-material__units units'>"+choice_array[response_data['units']]+'</td>'
        tr+="<td class='table-material__tags'>";
        tr+="<div class='tag__popup'>";
        JSON.parse(response_data['tag_list']).forEach(x=>{
          console.log(x.tag);
          tr+="<div class='tag-box'><p class='tag tag--flex'>" + x.tag + "</p></div>";
        });
        tr+="</div>";
        tr+="</td>";
        tr+="<td class='icon'>"
        tr+="<button class='update' data-toggle='modal' data-target='#UpdateMaterial'>" + edit_button_content + "</button>";
        tr+="<form class='delete_material' method='POST'><button class='remove' name='delete_material_sub' type='submit' onclick=\"return confirm('Opravdu chcete materiál smazat?')\">" + remove_button_content + "</button></form>";
        tr+="</td>"
        tr+='</tr>'
        table.innerHTML+=tr;
        tag_array=tag_array.concat(JSON.parse(response_data['tag_list']));
        material.push(response_data);
        console.log(response_data);
        console.log(response_data['tag_list']);
        console.log('done');
        $('#NewMaterial').modal('hide');
        CleanNewMaterialForm();
      }
    });
  });
  var new_material_modal=document.getElementById("NewMaterial");
  new_material_modal.addEventListener('show', function(e) {
    new_tag_array = [];
  });

  var update_material_modal=document.getElementById("UpdateMaterial");

  $("#UpdateMaterial").on('show.bs.modal', function(event) {
    console.log('update_modal');
    new_tag_array = [];
    $(this).find('div.tag__popup')[0].innerHTML='';
    $('form.update_material input#id_tag').val('');
    tag_array.filter(item => item.material_id === Number($('#material_id').val())).forEach(x=>{
      new_tag_array.push(x.tag);
      $(this).find('div.tag__popup')[0].innerHTML+="<div class='tag-box'><p class='tag tag--flex'>" + x.tag +"<button type='button' class='tag__button-close'><svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-x' viewBox='0 0 16 16'><path d='M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z'/></svg></button></p></div>";
    });
    console.log(new_tag_array);
  });
  $("#NewMaterial").on('show.bs.modal', function(event) {
    new_tag_array = [];
    console.log('new_material_modal');
  });


  $("form.update_material #id_tag").on("keydown",function search(e) {
    if(e.keyCode == 13) {
        e.preventDefault();
        console.log($(this).val());
        if(new_tag_array.includes($(this).val())===false){
          $("form.update_material div.tag__popup")[0].innerHTML+="<div class='tag-box'><p class='tag tag--flex'>" + $(this).val() +"<button type='button' class='tag__button-close'><svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-x' viewBox='0 0 16 16'><path d='M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z'/></svg></button></p></div>";
          new_tag_array.push($(this).val());
      };
        $(this).val('');
    }
  });
  $("form.new_material #id_tag").on("keydown",function search(e) {
    if(e.keyCode == 13) {
        e.preventDefault();
        console.log($(this).val());
        if(new_tag_array.includes($(this).val())===false){
          $("form.new_material div.tag__popup")[0].innerHTML+="<div class='tag-box'><p class='tag tag--flex'>" + $(this).val() +"<button type='button' class='tag__button-close'><svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-x' viewBox='0 0 16 16'><path d='M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z'/></svg></button></p></div>";
          new_tag_array.push($(this).val());
        };
        $(this).val('');
    }
  });
  function CleanNewMaterialForm() {
    $('form.new_material #new_material_name').val('');
    $('form.new_material #new_material_price').val('');
    $('form.new_material #new_material_margin').val('');
    $("form.new_material #new_material_units" ).val($("#new_material_units option:first").val());
    $("form.new_material div.tag-container")[0].innerHTML="";
  };

  $('form.new_material').on("click", "button.tag__button-close", function (event){
    var drop=$(this).closest('div.tag-box').text().trim();
    $(this).closest('div.tag-box').remove();
    new_tag_array=new_tag_array.filter(function(f) { return f !== drop });
  });

  $('form.update_material').on("click", "button.tag__button-close", function (event){
    var drop=$(this).closest('div.tag-box').text().trim();
    $(this).closest('div.tag-box').remove();
    new_tag_array=new_tag_array.filter(function(f) { return f !== drop });
  });

});
