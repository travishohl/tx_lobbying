(function (exports, $) {
  'use strict';
  var $paper = $('#notebook');
  var $nav = $('#breadcrumbs');

  var retrieve = function (url) {
    var $page = $('<article class="page"/>').appendTo($paper);
    // TODO don't use load, just do ajax and manually parse to get TITLE and
    var $index = $('<span class="page"/>').appendTo($nav);
    $.ajax(url, {
      dataType: 'html',
      success: function (data) {
        var $document = $('<div>' + data + '</div>');
        $page.append($document.find('div.page-content'));
        var title = $document.find('title').html() || 'TODO';
        $index.text(title);
      }
    });
    $page.data('notebook', {
      url: url,
      $index: $index,
      retrievedAt: Date.now()
    });
    $(window).scrollLeft(1e6);
  };

  var retrieveThis = function (e) {
    e.preventDefault();
    var $el = $(this);
    var $page = $el.closest('article.page');

    // clear notebook to the right
    $page.nextAll().remove();
    var $index = $page.data('notebook').$index;
    $index.nextAll().remove();

    $nav.append('<span class="link">' + $el.text() + '</span>');
    retrieve($el.attr('href'));

    $page.find('a.clicked').removeClass('clicked');
    $el.addClass('clicked');

    var $pageContent = $page.children().first();
    $pageContent.find('div.placeholder').remove();
    $('<div class="placeholder"/>').appendTo($pageContent)
      .css('top', $el.position().top + $el.outerHeight());
  };

  $paper.on('click', 'a', retrieveThis);

  // XXX side effect
  var $window = $(window);
  $window.on('scroll', function () {
    console.log($window.width(), $nav.width())
  });

  // exports
  exports.notebook = {
    retrieve: retrieve
  };

})(this, this.jQuery);
