const breakpoint = window.matchMedia('(max-width: 767px)');
let mySwiper;

const breakpointChecker = function () {
  if (breakpoint.matches === true) {
    if (mySwiper !== undefined) {
      mySwiper.destroy();
    }
    $('.suggestions .swiper-wrapper').addClass('row');
    $('.suggestions .suggestion').each((key, item) => {
      $(item)
        .removeClass('swiper-slide')
        .addClass('col-6')
        .addClass('col-sm-4');
    });
  } else if (breakpoint.matches === false)
    return enableSwiper();
};

const enableSwiper = function () {
  $('.suggestions .swiper-wrapper').removeClass('row');
  $('.suggestions .suggestion').each((key, item) => {
    $(item)
      .addClass('swiper-slide')
      .removeClass('col-6')
      .removeClass('col-sm-4');
  });
  mySwiper = new Swiper('.suggestions .swiper', {
    slidesPerView: 4,
    spaceBetween: 10,
    navigation: {
      prevEl: '.swiper-button-next',
      nextEl: '.swiper-button-prev',
    },
    breakpoints: {
      1000: {
        slidesPerView: 5,
      },
    },
  });
};


$(function () {
  $('.content-header .title').click((e) => {
    $('i', e.currentTarget).toggleClass('fa-rotate-180');
    $('.content-header .infos').animate({height: 'toggle'}, 200);
  });

  breakpoint.addListener(breakpointChecker);
  breakpointChecker();

  // bookmark
  const bookmarkBtn = $('.actions .bookmark');
  bookmarkBtn.click((e) => {
    if (!AuthenticationAlert()) return;
    const currentTarget = $(e.currentTarget);
    const url = currentTarget.data('url');

    $.ajax({
      url: url,
      method: bookmarkBtn.hasClass('bookmarked') ? 'DELETE' : 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      success(res) {
        if (this.method === 'DELETE') {
          currentTarget.removeClass('bookmarked');
          $('span', currentTarget).text('نشان کردن');
        } else {
          currentTarget.addClass('bookmarked');
          $('span', currentTarget).text('نشان شده');
        }
      },
      error(err) {
        ajaxErrorToast(err.status, 'خطایی هنگام نشانه گذاری به وجود آمد. لطفا بعدا امتحان کنید.');
      },
    })
  });

  // selected season episodes count
  const setEpisodesCount = () => {
    const episodesCount = $('.episodes-wrapper .episode').length
    $('.episodes-count').text(episodesCount);
  }
  setEpisodesCount();

  const selectSeason = (e) => {
    const clickedElement = $(e.currentTarget);
    if (clickedElement.hasClass('selected-season'))
      return

    const url = $('a', clickedElement).data('url');
    const episodesWrapper = $('.episodes-wrapper');
    const loading = $('.episodes-wrapper > .loading');

    $.ajax({
      url: url,
      beforeSend() {
        loading.show();
        $('.episodes-container', episodesWrapper).addClass('loading-episodes');
      },
      success(res) {
        $('.episodes-container', episodesWrapper).html(res);
        setEpisodesCount();
        episodeRating();

        $('.season.selected-season').removeClass('selected-season');
        clickedElement.addClass('selected-season');

        loading.hide();
        $('.episodes-container', episodesWrapper).removeClass('loading-episodes');
      },
      error(err) {
        loading.hide();
        $('.episodes-container', episodesWrapper).removeClass('loading-episodes');
        ajaxErrorToast(err.status, 'خطایی هنگام گرفتن قسمت ها به وجود آمد. لطفا بعدا امتحان کنید.');
      },
    })
  }
  $('.season').click(selectSeason);
});