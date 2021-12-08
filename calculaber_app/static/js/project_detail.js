$(document).ready(function(){
  $('#id_project_pic').on('change',function(){
    var filePath = $(this).val().split("\\");
    var fileName = filePath[filePath.length-1];
    $(this).next('.custom-file-label').html(fileName);
  });

  $("form.new_object #id_tag").on("keydown",function search(e) {
    if(e.keyCode == 13) {
        e.preventDefault();
        console.log($(this).val());
        if(new_tag_array.includes($(this).val())===false){
          $("form.new_object div.tag-container")[0].innerHTML+="<span class='badge rounded-pill bg-warning text-dark'>" + $(this).val() +"<button type='button' class='remove-tag'><svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='currentColor' class='bi bi-x' viewBox='0 0 16 16'><path d='M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z'/></svg></button></span>";
          new_tag_array.push($(this).val());
      };
        $(this).val('');
    }
  });

  $('form.new_object').on("click", "button.remove-tag", function (event){
    var drop=$(this).closest('span.badge').text().trim();
    $(this).closest('span.badge').remove();
    new_tag_array=new_tag_array.filter(function(f) { return f !== drop });
  });
//<option value="{{ item.id }}">{{item.name}} - {{item.project.name}}</option>
  $("#DuplicateObject").on('show.bs.modal', function(event) {
    console.log('duplicate_object_modal');
    $(this).find('select#ObjectSelect')[0].innerHTML='';
    all_objects.forEach(x=>{
      $(this).find('select#ObjectSelect')[0].innerHTML+="<option value=" + x.id + ">" + x.name + " - " + x.project__name + "</option>";
    });
  });
  $("#DuplicateObject input#object_search").on("keydown",function search(e) {
    if(e.keyCode == 13) {
      e.preventDefault();
    };
  });
  $("#DuplicateObject input#object_search").on("keyup",function search(e) {
    e.preventDefault();
    console.log($(this).val());
    if(e.keyCode == 13) {
      //var temp=tag_array.filter(item => item.tag.toLowerCase().indexOf($(this).val().toLowerCase()) >=0);
      //var unique_temp=tag_array.map(item => item.object_id).filter((value, index, self) => self.indexOf(value) === index)
      var search=[];
      search=search.concat(tag_array.filter(item => item.tag.toLowerCase().indexOf($(this).val().toLowerCase()) >=0).map(item => item.object_id));
      search=search.concat(all_objects.filter(item => item.name.toLowerCase().indexOf($(this).val().toLowerCase()) >=0).map(item => item.id));
      search=search.filter((value, index, self) => self.indexOf(value) === index);
      console.log(search);
      $("#DuplicateObject select#ObjectSelect")[0].innerHTML='';
      all_objects.filter(item => search.includes(item.id)).forEach(x=>{
        $("#DuplicateObject select#ObjectSelect")[0].innerHTML+="<option value=" + x.id + ">" + x.name + " - " + x.project__name + "</option>";
      });

    };
  });

  //continue here
  $("form.duplicate_object").submit(function(e){
    e.preventDefault();
    $.ajax({
      url:'',
      type:'post',
      data:{
        id:$('select#ObjectSelect').val(),
        project:project[0].id,
        type:'duplicate',
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()},
      error: function (request, error) {
        console.log(arguments);
        alert(" Can't do because: " + error);
      },
      success: function(response){
        response_data=response;
        var object_response=JSON.parse(response_data['object']);
        console.log(response_data['object']);
        tag_array=tag_array.concat(JSON.parse(response_data['tag_list']));
        objects=objects.concat(object_response)
        console.log(tag_array);
        delete response_data['tag_list'];
        console.log('done');
        new_tag_array=[];
        $('form.new_object #id_name').val(),
        $("form.new_object div.tag-container")[0].innerHTML="";
        $('#DuplicateObject').modal('hide');
        document.getElementById("object-cards").innerHTML+=GenerateObjectCard(object_response[0].id,object_response[0].name,object_response[0].object_price,object_response[0].create_date);
        $("h3.total_price")[0].innerHTML=FormatNumber(objects.map(item => item.object_price).reduce((prev, next) => Number(prev) + Number(next))) + " CZK";
      }
    })
  });

  $("form.new_object").submit(function(e){
    e.preventDefault();
    $.ajax({
      url:'',
      type:'post',
      data:{
        name:$('form.new_object #id_name').val(),
        project:project[0].id,
        tags:new_tag_array,
        type:'new',
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()},
      error: function (request, error) {
        console.log(arguments);
        alert(" Can't do because: " + error);
      },
      success: function(response){
        response_data=response;
        tag_array=tag_array.concat(JSON.parse(response_data['tag_list']));
        console.log(tag_array);
        delete response_data['tag_list'];
        objects.push(response_data);
        console.log('done');
        new_tag_array=[];
        $('form.new_object #id_name').val(),
        $("form.new_object div.tag-container")[0].innerHTML="";
        $('#NewObject').modal('hide');
        document.getElementById("object-cards").innerHTML+=GenerateObjectCard(response_data['id'],response_data['name'],0,response_data['create_date']);
      }
    });
  });
});
