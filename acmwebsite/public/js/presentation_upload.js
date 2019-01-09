(function() {
  const add_file = $('#add_file');
  const file_list = $('#file_list');

  let i = 0;

  add_file.click(() => {
    (function(rowid) { // Closure of the id
      file_list.append(`
        <tr id="file-${rowid}">
          <td><input type="text" name="filedesc-${rowid}" required /></td>
          <td><input type="file" name="fileupload-${rowid}" required /></td>
          <td><button id="delete-${rowid}" type="button" class="btn btn-danger"><i class="fa fa-times"></i></button></td>
        </tr>
      `);

      $(`#delete-${rowid}`).click(() => {
        $(`#file-${rowid}`).remove();
      });
    })(i);

    i++;
  });
})();
