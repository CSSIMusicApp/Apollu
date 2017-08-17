var setup = () => {
  $('#show-more').click(() => {
    var prop = $('#show-more-form').serialize();

    $.ajax({
      url: '/',
      method: 'POST',
      data: { },
    }).done(function(response){
      console.log('done')
    }).fail(function() {
      console.log('failed')
    })
  })


}

$(document).ready(setup);
