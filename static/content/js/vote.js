const AuthenticationAlert = () => {
  if (!isAuthenticated) {
    const loginUrl = '/users/login/?next=' + window.location.pathname
    swal.fire({
      icon: 'error',
      buttonsStyling: false,
      focusConfirm: false,
      title: `لطفا ابتدا وارد حساب کاربری خود شوید.`,
      confirmButtonText: `<a href="${loginUrl}" class="btn btn-primary btn-lg visible">ورود</a>`,
    });
    return false
  }
  return true
}

const episodeRating = () => {
  $('.episode-rating .like').click((e) => {
    const currentTarget = $(e.currentTarget);
    if (!AuthenticationAlert()) return;
    const url = currentTarget.data('url');

    $.ajax({
      url: url,
      method: currentTarget.hasClass('liked') ? 'DELETE' : 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      success(res) {
        if (this.method === 'POST') {
          currentTarget.addClass('liked');
          // remove disliked class from episode dislike button which is back of the like button
          currentTarget.next().removeClass('disliked');
        } else
          currentTarget.removeClass('liked');
      },
      error(err) {
        ajaxErrorToast(err.status, 'خطایی هنگام امتیازدهی به وجود آمد. لطفا بعدا امتحان کنید.');
      },
    });
  });
  $('.episode-rating .dislike').click((e) => {
    const currentTarget = $(e.currentTarget);
    if (!AuthenticationAlert()) return;
    const url = currentTarget.data('url');

    $.ajax({
      url: url,
      method: currentTarget.hasClass('disliked') ? 'DELETE' : 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      success(res) {
        if (this.method === 'POST') {
          currentTarget.addClass('disliked');
          // remove liked class from episode like button which is next to the dislike button
          currentTarget.prev().removeClass('liked');
        } else
          currentTarget.removeClass('disliked');
      },
      error(err) {
        ajaxErrorToast(err.status, 'خطایی هنگام امتیازدهی به وجود آمد. لطفا بعدا امتحان کنید.');
      },
    });
  });
}

$(function () {
  $('.actions .like').click((e) => {
    const currentTarget = $(e.currentTarget);
    if (!AuthenticationAlert()) return;
    const url = currentTarget.data('url');

    $.ajax({
      url: url,
      method: currentTarget.hasClass('liked') ? 'DELETE' : 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      success(res) {
        if (this.method === 'POST') {
          currentTarget.addClass('liked');
          $('.actions .dislike').removeClass('disliked');
        } else
          currentTarget.removeClass('liked');
      },
      error(err) {
        ajaxErrorToast(err.status, 'خطایی هنگام امتیازدهی به وجود آمد. لطفا بعدا امتحان کنید.');
      },
    });
  });

  $('.actions .dislike').click((e) => {
    const currentTarget = $(e.currentTarget);
    if (!AuthenticationAlert()) return;
    const url = currentTarget.data('url');

    $.ajax({
      url: url,
      method: currentTarget.hasClass('disliked') ? 'DELETE' : 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      success(res) {
        if (this.method === 'POST') {
          currentTarget.addClass('disliked');
          $('.actions .like').removeClass('liked');
        } else
          currentTarget.removeClass('disliked');
      },
      error(err) {
        ajaxErrorToast(err.status, 'خطایی هنگام امتیازدهی به وجود آمد. لطفا بعدا امتحان کنید.');
      },
    });
  });

  episodeRating();
});
