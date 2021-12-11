$('#id_project_pic').on('change',function(){
  var filePath = $(this).val().split("\\");
  var fileName = filePath[filePath.length-1];
  $(this).next('.custom-file-label').html(fileName);
});

$("#NewProject").on('show.bs.modal', function(event) {
  console.log('new_project_modal');
  $("form.new-project").get(0).reset();
  $('#id_project_pic').next('.custom-file-label').html('Vyber obrázek...')
});
