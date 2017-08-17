function setup()
{
  $('#text-data').hide()
  $('.videourl').hide()
  $('#input-fields').hide()

  $('input:radio[name="sectiononetype"]').on('click', function() {
    if (this.checked && this.value == 'post') {
      $('#input-fields').show()
      $('#input-fields').css("top", "60%")
      $('#text-data').show()
      $('.videourl').hide()
  }

  if (this.checked && this.value == 'video') {
    $('#input-fields').show()
    $('#input-fields').css("top", "40%")
    $('#text-data').hide()
    $('.videourl').show()
  }
})
}

$(document).ready(setup);
