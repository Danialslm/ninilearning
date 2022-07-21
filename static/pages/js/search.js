$(function () {
  const searchInput = $('.search-form input');

  let typingTimer;
  searchInput.on('input', (e) => {
    cleanSearchResults();
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doSearch, 1000);
  });

  const cleanSearchResults = () => {
    $('.search-results').html('');
  }

  $('.search-form .clean').click(() => {
    searchInput.val('');
    cleanSearchResults();
  });

  const doSearch = () => {
    const query = $('.search-form input').val();
    if (!query || query.length < 3)
      return

    $.ajax({
      url: window.location.pathname + `?query=${query}`,
      beforeSend() {
        $('.loading').show();
      },
      success(res) {
        $('.search-results').html(res);
        $('.loading').hide();
      },
      error(err) {
        $('.loading').hide();
        ajaxErrorToast(err.status, 'خطایی هنگام گرفتن اطلاعات به وجود آمد. لطفا بعدا امتحان کنید.');
      },
    });
  }

  $('.search-form').submit((e) => {
    e.preventDefault();
  });
});