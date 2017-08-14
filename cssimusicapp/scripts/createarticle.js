function setup()
{
  $('.writtenpost').hide()
  $('.videourl').hide()
  $('.spotifyurl').hide()

  $('input:radio[name="sectiononetype"]').on('click', function() {
    if (this.checked && this.value == 'post') {
      $('.writtenpost').show()
      $('.videourl').hide()
      $('.spotifyurl').hide()
  }

  if (this.checked && this.value == 'video') {
    $('.writtenpost').hide()
    $('.videourl').show()
    $('.spotifyurl').hide()
  }

  if (this.checked && this.value == 'playlist') {
    $('.writtenpost').hide()
    $('.videourl').hide()
    $('.spotifyurl').show()
  }
})
}

$(document).ready(setup);
