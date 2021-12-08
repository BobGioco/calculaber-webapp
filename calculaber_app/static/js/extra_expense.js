$(document).ready(function(){
  $("table").on("submit","form.delete_extra_expense",function(e){
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
        extra_expense=extra_expense.filter(item => item.id!=item_id)
        var row = document.getElementById(item_id);
        row.parentNode.removeChild(row);
        console.log(response_data);
        $("h4 span.total_price").text(FormatNumber(extra_expense.map(item => item.price).reduce((prev, next) => Number(prev) + Number(next))) + " Kč")
        console.log('done');
      }
    });
  });

  //$('button.update').click(function (event){
  $('table').on("click", "button.update", function (event){
        console.log('hi');
   var index = Number($(this).closest('tr').attr('id'));
   var temp_data=extra_expense.find(item => item.id === index);
   $('#extra_expense_id').attr('value',index);
   $('#update_expense_name').val(temp_data['name']);
   $('#update_expense_price').val(temp_data['price']);
   $('#update_expense_description').val(temp_data['description']);
  });

  $("form.update_extra_expense").submit(function(e){
    e.preventDefault();
    $.ajax({
      url:'',
      type:'post',
      data:{
        item_id:$('#extra_expense_id').val(),
        project_id:project_id,
        name:$('#update_expense_name').val(),
        price:$('#update_expense_price').val(),
        description:$('#update_expense_description').val(),
        type:'update',
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()},
      error: function (request, error) {
        console.log(arguments);
        alert(" Can't do because: " + error);
      },
      success: function(response){
        response_data=response;
        $('#' + response_data['id'] + " td.name").text(response_data['name']);
        $('#' + response_data['id'] + " td.description").text(response_data['description']);
        $('#' + response_data['id'] + " td.price").text(FormatNumber(response_data['price']) + ' Kč');

        var to_update_data=extra_expense.findIndex(item => item.id === response_data['id']);
        extra_expense[to_update_data]=response_data;
        $("h4 span.total_price").text(FormatNumber(extra_expense.map(item => item.price).reduce((prev, next) => Number(prev) + Number(next))) + " Kč")
        console.log('done');
        $('#UpdateExtraExpense').modal('hide');
      }
    });
  });

  $("form.new_extra_expense").submit(function(e){
    e.preventDefault();
    $.ajax({
      url:'',
      type:'post',
      data:{
        name:$('#new_expense_name').val(),
        project_id:project_id,
        description:$('#new_expense_description').val(),
        price:$('#new_expense_price').val(),
        type:'new',
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()},
      error: function (request, error) {
        console.log(arguments);
        alert(" Can't do because: " + error);
      },
      success: function(response){
        response_data=response;
        var table = document.getElementById("extra_expense_detail_tbl").getElementsByTagName("tbody")[0];
        tr="";
        tr+="<tr id='" + response_data['id'] + "'>";
        tr+="<td class='name'>"+response_data['name']+"</td>"+"<td class='description'>"+response_data['description']+"</td>"+"<td class='price'>"+FormatNumber(response_data['price'])+" Kč</td>";
        tr+="<td>";
        tr+="<button type='button' class='btn btn-primary update' data-toggle='modal' data-target='#UpdateExtraExpense'>Upravit</button>";
        tr+="<form class='delete_extra_expense' method='POST'><input class='btn btn-danger' name='delete_extra_expense_sub' type='submit' onclick=\"return confirm('Opravdu chcete výdaj smazat?')\" value='Smazat'></form>";
        tr+="</td>";
        tr+='</tr>';
        table.innerHTML+=tr;
        extra_expense.push(response_data);
        $("h4 span.total_price").text(FormatNumber(extra_expense.map(item => item.price).reduce((prev, next) => Number(prev) + Number(next))) + " Kč")
        console.log('done');
        $('#NewExtraExpense').modal('hide');
        CleanNewExpenseForm();
      }
    });
  });

  $("#UpdateExtraExpense").on('show.bs.modal', function(event) {
    console.log('update_modal');
  });
  $("#NewExtraExpense").on('show.bs.modal', function(event) {
    console.log('new_modal');
  });


  function CleanNewExpenseForm() {
    $('form.new_extra_expense #new_expense_name').val('');
    $('form.new_extra_expense #new_expense_price').val('');
    $('form.new_extra_expense #new_expense_description').val('');
  };


});
