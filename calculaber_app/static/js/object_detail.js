$(document).ready(function(){
  //$("form.delete_material").submit(function(e){
  $("table").on("submit","form.delete_materialobject",function(e){
    e.preventDefault();
    var item_id=$(this).closest('tr').attr("id");
    console.log($("table.table input[name=csrfmiddlewaretoken]").val());
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
        var row = document.getElementById(item_id);
        row.parentNode.removeChild(row);
        materialobjects=materialobjects.filter(item => item.id!=item_id)
        console.log(response_data);
        console.log('done');
      }
    });
  });
  $("form.update_material_object").submit(function(e){
    e.preventDefault();
    $.ajax({
      url:'',
      type:'post',
      data:{
        item_id:$('#materialobject_id').val(),
        name:$('#id_name_update').val(),
        amount:$('#id_amount_update').val(),
        customized:$("#id_customized_update").prop("checked"),
        price:$('#id_price_update').val(),
        margin:$("#id_margin_update").val(),
        type:'update',
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()},
      error: function (request, error) {
        console.log(arguments);
        alert(" Can't do because: " + error);
      },
      success: function(response){
        //continued
        response_data=response;
        var to_update_data=materialobjects.findIndex(item => item.id === response_data['id']);
        materialobjects[to_update_data]=response_data;
        $('tr#' + response_data['id'] + " td.name").text(response_data['name']);
        $('tr#' + response_data['id'] + " td.amount").text(FormatNumber(response_data['amount']) + ' ' + units[response_data['material__units']]);
        if(response_data['customized']===true){
          $('tr#' + response_data['id'] + " td.price").text(FormatNumber(response_data['price']) + ' Kč');
          $('tr#' + response_data['id'] + " td.margin").text(FormatNumber(response_data['margin']) + ' %');
        }else {
          $('tr#' + response_data['id'] + " td.price").text(FormatNumber(response_data['material__price']) + ' Kč');
          $('tr#' + response_data['id'] + " td.margin").text(FormatNumber(response_data['material__margin']) + ' %');
        }
        $('tr#' + response_data['id'] + " td.total").text(FormatNumber(response_data['total_price']) + ' Kč');

        $('span.total_object_price')[0].innerHTML=FormatNumber(materialobjects.map(item => item.total_price).reduce((prev, next) => Number(prev) + Number(next))) + " Kč";
        console.log('materialobject update');
        console.log('done');
        $('#UpdateMaterialObject').modal('hide');
      }
    });
  });


  function GenerateSelect(id,name,price,units){
    var _ = "";
    if(units==="m2"){
      _="<option value=" + id + ">" + name + " (m<sup>2</sup></td>; " + FormatNumber(price) + "Kč)</option>";
    }else if(units==="m3"){
      _="<option value=" + id + ">" + name + " (m<sup>3</sup></td>; " + FormatNumber(price) + "Kč)</option>";
    }else{
      _="<option value=" + id + ">" + name + " (" + units + '; ' + FormatNumber(price) + "Kč)</option>";
    }
    return _
  };

  function UnitSelect(units){
    var _ = "";
    if(units==="m2"){
      _="m<sup>2</sup>";
    }else if(units==="m3"){
      _="m<sup>3</sup>";
    }else{
      _=units;
    }
    return _
  }


  $("#NewMaterialObject input#material_search").on("keydown",function search(e) {
    if(e.keyCode == 13) {
      e.preventDefault();
    };
  });
  $("#NewMaterialObject input#material_search").on("keyup",function search(e) {
    e.preventDefault();
    console.log($(this).val());
    if(e.keyCode == 13) {
      //var temp=tag_array.filter(item => item.tag.toLowerCase().indexOf($(this).val().toLowerCase()) >=0);
      //var unique_temp=tag_array.map(item => item.object_id).filter((value, index, self) => self.indexOf(value) === index)
      var search=[];
      search=search.concat(material_tags.filter(item => item.tag.toLowerCase().indexOf($(this).val().toLowerCase()) >=0).map(item => item.material_id));
      search=search.concat(material.filter(item => item.name.toLowerCase().indexOf($(this).val().toLowerCase()) >=0).map(item => item.id));
      search=search.filter((value, index, self) => self.indexOf(value) === index);
      console.log(search);
      $("#NewMaterialObject select#material_select")[0].innerHTML='';
      material.filter(item => search.includes(item.id)).forEach(x=>{
        $("#NewMaterialObject select#material_select")[0].innerHTML+=GenerateSelect(x.id,x.name,x.price,units[x.units])
      });

    };
  });
  $('table#object_detail_tbl').on("click", "button.update", function (event){
     var index = Number($(this).closest('tr').attr('id'));
     var temp_data=materialobjects.find(item => item.id === index);
     console.log("INDEX: " + index)
     console.log(temp_data);
     console.log(temp_data['amount']);
     $('#materialobject_id').attr('value',index);
     //$('#id_name_update').attr('value',temp_data['name']);
     $('#id_name_update').val(temp_data['name']);
     //$('#id_amount_update').attr('value',temp_data['amount']);
     $('#id_amount_update').val(temp_data['amount']);
     $('span#amount_units')[0].innerHTML=UnitSelect(units[temp_data['material__units']]);
     if(temp_data['customized']===true){
       $('#id_customized_update').prop('checked', true);
       $('div.check_box_true').attr("hidden",false);
       //$('#id_margin_update').attr('value',temp_data['margin']);
       //$('#id_price_update').attr('value',temp_data['price']);
       $('#id_margin_update').val(temp_data['margin']);
       $('#id_price_update').val(temp_data['price']);
     }else{
       $('#id_customized_update').prop('checked', false);
       $('div.check_box_true').attr("hidden",true);
       $('#id_margin_update').val('');
       $('#id_price_update').val('');
     }

    }
  );

  $("form.new_material_object").submit(function(e){
    e.preventDefault();
    $.ajax({
      url:'',
      type:'post',
      data:{
        name:$('#id_name').val(),
        amount:$('#id_amount').val(),
        material_id:$('select#material_select').val(),
        object_id:object.id,
        type:'new',
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()},
      error: function (request, error) {
        console.log(arguments);
        alert(" Can't do because: " + error);
      },
      success: function(response){
        response_data=response;
        console.log(response_data);
        var table = document.getElementById("object_detail_tbl").getElementsByTagName("tbody")[0];
        table.innerHTML+=GenerateRow(response_data['id'],response_data['name'],response_data['material__name'],response_data['amount'],response_data['material__units'],response_data['material__price'],response_data['material__margin'],response_data['total_price']);
        materialobjects.push(response_data);
        console.log('done');
        $('span.total_object_price')[0].innerHTML=FormatNumber(materialobjects.map(item => item.total_price).reduce((prev, next) => Number(prev) + Number(next))) + " Kč";
        $('#NewMaterialObject').modal('hide');
        CleanNewMaterialObjectForm();
      }
    });
  });
  function CleanNewMaterialObjectForm() {
    $('form.new_material_object #id_name').val('');
    $('form.new_material_object #id_amount').val('');
    $('form.new_material_object #material_search').val('');
    $("form.new_material_object #material_select" ).innerHTML="";
  };

  function CleanUpdateMaterialObjectForm() {
    $('form.update_material_object #id_name_update').val('');
    $('form.update_material_object #id_amount_update').val('');
    $("#id_customized_update").prop("checked",false);
    $('#id_price_update').val('');
    $("#id_margin_update").val('');
  };
  $("#NewMaterialObject").on('show.bs.modal', function(event) {
    console.log('new_material_object_modal');
    $(this).find('select#material_select')[0].innerHTML='';
    material.forEach(x=>{
      $(this).find('select#material_select')[0].innerHTML+=GenerateSelect(x.id,x.name,x.price,units[x.units]);
    });
  });

  $("#UpdateMaterialObject").on('show.bs.modal', function(event) {
    console.log('update_material_object_modal');
  });
  $('#id_customized_update').click(function(){
    if($(this).prop("checked")==true){
      $('.check_box_true').attr("hidden",false);
    }else if($(this).prop("checked")==false){
      $('.check_box_true').attr("hidden",true);
    }
  });
  $("#UpdateObject").on('show.bs.modal', function(event) {
    console.log('update_object_modal');
    new_tag_array=[];
    $('form.update_object #update_object_name').val(object.name);
    $(this).find('div.tag-container')[0].innerHTML='';
    $('form.update_object input#id_tag').val('');
    object_tags.forEach(x=>{
      new_tag_array.push(x.tag);
      $(this).find('div.tag-container')[0].innerHTML+="<span class='badge rounded-pill bg-warning text-dark'>" + x.tag +"<button type='button' class='remove-tag'><svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-x' viewBox='0 0 16 16'><path d='M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z'/></svg></button></span>";
    });
  });
  $('form.update_object').on("click", "button.remove-tag", function (event){
    var drop=$(this).closest('span.badge').text().trim();
    $(this).closest('span.badge').remove();
    new_tag_array=new_tag_array.filter(function(f) { return f !== drop });
  });
  $("form.update_object #id_tag").on("keydown",function search(e) {
    if(e.keyCode == 13) {
        e.preventDefault();
        console.log($(this).val());
        if(new_tag_array.includes($(this).val())===false){
          $("form.update_object div.tag-container")[0].innerHTML+="<span class='badge rounded-pill bg-warning text-dark'>" + $(this).val() +"<button type='button' class='remove-tag'><svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-x' viewBox='0 0 16 16'><path d='M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z'/></svg></button></span>";
          new_tag_array.push($(this).val());
        };
        $(this).val('');
    }
  });



  $("form.update_object").submit(function(e){
    e.preventDefault();
    $.ajax({
      url:'',
      type:'post',
      data:{
        item_id:object.id,
        name:$('#update_object_name').val(),
        tags:new_tag_array,
        type:'update_object',
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()},
      error: function (request, error) {
        console.log(arguments);
        alert(" Can't do because: " + error);
      },
      success: function(response){
        response_data=response;
        object.name=response_data.name;
        $('h1.header__title').text(object.name);
        tr="";
        JSON.parse(response_data['tag_list']).forEach(x=>{
          tr+="<div class='tag-box'><p class='tag'>" + x.tag + "</p></div>"
        });
        $('div.tag__header')[0].innerHTML=tr;
        object_tags=JSON.parse(response_data['tag_list']);
        console.log('done');
        $('#UpdateObject').modal('hide');
      }
    });
  });


});
