$(document).ready(function() {

    //ICONFONT FALLBACK (Polyfill for no fontface support. Slightly Modified  - (c) 2012: John Polacek http://dfcb.github.com/iconfont-fallback. Dual MIT & GPL license)
    
    ;(function($) {

      $.fn.iconfontFallback = function(options) {
        var $target = this,
            defaults = {iconDir:'../images/icon_fallbacks'},
            settings = $.extend({}, defaults, options);

        $target.each(function() {
            var classes = $(this).attr('class').split(' ');
            for (var i = 0; i < classes.length; i++) {
                var iconClass = /^icon\_(.+)/.exec(classes[i]); }
            if (iconClass) {
                if ($(this).hasClass('button')) {
                    var iconName = iconClass[1] +'_white.png';
                }
                else if ($(this).is('a') && !$(this).hasClass('button')) {
                    var iconName = iconClass[1] +'_link.png';
                }
                else {
                    var iconName = iconClass[1] +'_text.png'
                }
                $(this)
                    .prepend('<img src="'+settings.iconDir+'/'+iconName+'" />')
                    .addClass('icon-fallback');
            }
        });

        return $target;
      };

    }(jQuery));

    // ICON FONT FALLBACK

    if (!$('html').hasClass('fontface')) {
        $('[class*="icon_"]').iconfontFallback();
    }

}