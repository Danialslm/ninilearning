$(function () {
  const discountForm = $('.discount-form form');
  $('.discount-form h3').click((e) => {
    $('i.fa-chevron-left', e.currentTarget).toggleClass('rotate-down');
    discountForm.animate({height: 'toggle'}, 200);
  });
});