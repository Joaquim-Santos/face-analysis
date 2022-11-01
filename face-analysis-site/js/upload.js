$(function() {

  $('#theForm').on('submit', sendFile);
});

function sendFile(e) {
    e.preventDefault();

    // get the reference to the actual file in the input
    var theFormFile = $('#theFile').get()[0].files[0];

    $.ajax({
      type: 'PUT',
      url: 'https://s3.amazonaws.com/face-analysis-images/output/',
      // Content type must much with the parameter you signed your URL with
      contentType: 'binary/octet-stream',
      // this flag is important, if not set, it will try to send data as a form
      processData: false,
      // the actual file is sent raw
      data: theFormFile
    })
    .success(function() {
      alert('File uploaded');
    })
    .error(function() {
      alert('File NOT uploaded');
      console.log( arguments);
    });

    return false;
  });
}