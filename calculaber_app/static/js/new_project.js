$('#id_project_pic').on('change',function(){
                var filePath = $(this).val().split("\\");
                var fileName = filePath[filePath.length-1];
                $(this).next('.custom-file-label').html(fileName);
            });
