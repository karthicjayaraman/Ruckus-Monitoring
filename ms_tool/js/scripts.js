$(document).ready(function() {

    // Target IE 10 == Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)

    var b = document.documentElement;
    b.setAttribute('data-useragent',  navigator.userAgent);
    b.setAttribute('data-platform', navigator.platform );

    // :active CLASS SUPPORT FOR TOUCH DEVICES
    
    document.addEventListener("touchstart", function() {},false);

    // SIDENAV MOBILE TOGGLE

    $('.mobile_menu_toggle a').click(function (e) {
        $('.sidenav').toggleClass('expand');
        $(this).toggleClass('icon_arrow_up').toggleClass('icon_arrow_down');
        e.preventDefault();
    });

    // SIDENAV BEHAVIOR

    var newHash = "";
    
    $('.sidenav > li').click(function () {
        if (!$('ul', this).hasClass('expand')) {
            $('.sidenav ul.expand').removeClass('expand');
            $('ul', this).addClass('expand');
            $(this).addClass('current');
        }
        if (!$(this).has('ul').length) {
            $('.sidenav ul.expand').removeClass('expand');
            $('.sidenav li').removeClass('current');
            $(this).addClass('current');
        }
    });

    $('a[href="#"]').click(function (e) {
        e.preventDefault();
    });
    
    $(window).bind('hashchange', function() {
    
        newHash = window.location.hash.substring(1);
        var checkElement = $(".sidenav a[href='#"+newHash+"']");
        
        if (newHash) {
            $('.sidenav li').removeClass('current');
            $(checkElement).closest('li').addClass('current');
            $(checkElement).parents('.folder').addClass('current');

            if (!$(checkElement).parents('.folder').length) {
                $('.sidenav ul.expand').removeClass('expand');
            }
            
            if ($(checkElement).parents('.folder').length && (!$(checkElement).parents('.folder > ul').hasClass('expand'))) {
                $('.sidenav ul.expand').removeClass('expand');
                checkElement.closest('ul').addClass('expand');
            } else {
                $('.sidenav').removeClass('expand');
                $('.mobile_menu_toggle a').removeClass('icon_arrow_up').addClass('icon_arrow_down');
            }
        }
        
    });
    
    $(window).trigger('hashchange');

    // SELECT ALL TEXT INSIDE CODE ELEMENTS

    jQuery.fn.selectText = function(){
        var doc = document;
        var element = this[0];
        if (doc.body.createTextRange) {
            var range = document.body.createTextRange();
            range.moveToElementText(element);
            range.select();
        } else if (window.getSelection) {
            var selection = window.getSelection();
            var range = document.createRange();
            range.selectNodeContents(element);
            selection.removeAllRanges();
            selection.addRange(range);
        }
    };

    //ICONFONT FALLBACK (Polyfill for no fontface support)

    /*  
    Modded by: Josh Holloran for Aruba Networks
    Author: (c) 2012: John Polacek http://dfcb.github.com/iconfont-fallback. Dual MIT & GPL license
    */
    
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
                    var iconName = iconClass[1] +'_text.png';
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

    // ICON LIGATURES FALLBACK

    (function () {
        'use strict';
        function supportsProperty(p) {
            var prefixes = ['Webkit', 'Moz', 'O', 'ms'],
                i,
                div = document.createElement('div'),
                ret = p in div.style;
            if (!ret) {
                p = p.charAt(0).toUpperCase() + p.substr(1);
                for (i = 0; i < prefixes.length; i += 1) {
                    ret = prefixes[i] + p in div.style;
                    if (ret) {
                        break;
                    }
                }
            }
            return ret;
        }
        if (!supportsProperty('fontFeatureSettings')) {
            $('html').addClass('noliga');
        }
    }());

}); // END DOCUMENT READY

// TABS

function tabs() {
    $('.tabcontrols').find('li:eq(0)').addClass('current');
    $('.tabs').find('> div:eq(0)').nextAll().hide();
    $('.tabcontrols li a').on('click', function (e) {
        $(this).parent().siblings().removeClass('current');
        $(this).closest('.tabs').find('> div').hide();
        $(this).parent().addClass('current');
        var index = $(this).closest('.tabs').find('.tabcontrols li a').index(this);
        $(this).closest('.tabs').find('select').prop('selectedIndex', index);
        $(this).closest('.tabs').find('> div:eq('+index+')').show();
        e.preventDefault();
    });
}

// RESPONSIVE TABS (Tabs become selects)

/*  Modded by: Josh Holloran for Aruba Networks
    Author: http://tinynav.viljamis.com v1.03 by @viljamis
*/

(function ($, window, i) {
  $.fn.tinyNav = function (options) {

    // Default settings
    var settings = $.extend({
      'active' : 'current', // String: Set the "active" class
      'header' : false // Boolean: Show header instead of the active item
    }, options);

    return this.each(function () {

      // Used for namespacing
      i++;

      var $nav = $(this),
        // Namespacing
        namespace = 'tinynav',
        namespace_i = namespace + i,
        l_namespace_i = '.l_' + namespace_i,
        $select = $('<select/>').addClass(namespace + ' ' + namespace_i);

      if ($nav.is('ul,ol')) {

        if (settings.header) {
          $select.append(
            $('<option/>').text('Navigation')
          );
        }

        // Build options
        var options = '';

        $nav
          .addClass('l_' + namespace_i)
          .find('li a')
          .each(function () {
            options +=
              '<option>' +
              $(this).text() +
              '</option>';
          });

        // Append options into a select
        $select.append(options);

        // Select the active item
        if (!settings.header) {
          $select
            .find(':eq(' + $(l_namespace_i + ' li a')
            .index($(l_namespace_i + ' li.' + settings.active)) + 'a)')
            .attr('selected', true);
        }

        // Change window location
        $select.change(function () {
            var index = $select.prop('selectedIndex');
            $(l_namespace_i + ' li').removeClass(settings.active);
            $(l_namespace_i + ' li:eq('+index+')').addClass(settings.active);
            $select.closest('.tabs').find('> div').hide();
            $select.closest('.tabs').find('> div:eq('+index+')').show();
        });

        // Inject select
        $(l_namespace_i).after($select);

      }

    });

  };
})(jQuery, this, 0);

// OFF CANVAS

function offcanvas() {

    $('.off_canvas_toggle').on('click', function (e) {
        $(this).closest('.off_canvas_wrap').toggleClass('move_right');
        $('.off_canvas_menu ul.expand').removeClass('expand');
        $('.off_canvas_menu .folder > a > span').removeClass('icon_collapse').addClass('icon_expand');
        e.preventDefault();
    });

    $('.exit_off_canvas').on('click', function (e) {
        $('.off_canvas_wrap').removeClass('move_right');
        $('.off_canvas_menu ul.expand').removeClass('expand');
        $('.off_canvas_menu .folder > a > span').removeClass('icon_collapse').addClass('icon_expand');
        e.preventDefault();
    });

    $('.off_canvas_menu .folder > a > span').on('click', function (e) {
        if ($(this).parents('.folder').length && (!$(this).parent().next('ul').hasClass('expand'))) {
            $('.off_canvas_menu ul.expand').removeClass('expand');
            $(this).parent().next('ul').addClass('expand');
            $('.off_canvas_menu .folder > a > span').removeClass('icon_collapse').addClass('icon_expand');
            $(this).addClass('icon_collapse').removeClass('icon_expand');
        }
        else if ($(this).parents('.folder').length && ($(this).parent().next('ul').hasClass('expand'))) {
            $('.off_canvas_menu ul.expand').removeClass('expand');
            $('.off_canvas_menu .folder > a > span').removeClass('icon_collapse').addClass('icon_expand');
        }
        e.preventDefault();
    });
}

// PILLS & SEGMENTED CONTROL

function pills() {
    $('.pills li a, .seggyc li a').on('click', function (e) {
        $(this).parent().siblings().removeClass('current');
        $(this).parent().addClass('current');
        e.preventDefault();
    });
}

// DROPDOWNS

function dropdowns() {

    $(document).on('click', function () {
        $('.dropdown').removeClass('focus');
    });

    $('.dropdown > a, .dropdown > div > a').on('click', function (e) {
        $('.dropdown').not($(this).parents()).removeClass('focus');
        $(this).closest('.dropdown').toggleClass('focus');
        e.preventDefault();
        e.stopPropagation();
    });

    $('.panel .title_heading .dropdown ul').on('click', function (e) {
        e.stopPropagation();
    });
}

// GLOBAL ALERT TRIGGERS

function alerts() {

    $(document).on('click', function () {
        $('.global_alert').removeClass('visible');
    });

    $('.global_alerts .button').on('click', function (e) {
        $('.global_alert').removeClass('visible');
        var target_category = $(this).attr('data-target_category');
        $('.global_alert.' + target_category).addClass('visible');
        e.preventDefault();
        e.stopPropagation();
    });
}

// MODAL OVERLAY

function overlay() {
    $('.modals a.confirmation').on('click', function () {
        $('.content_wrapper').addClass('overlay_open');
        $('.overlay.light').addClass('open');
        $('.message.signup').hide();
        $('.message.confirmation').show();
    });

    $('.modals a.signup').on('click', function () {
        $('.content_wrapper').addClass('overlay_open');
        $('.overlay.heavy').addClass('open');
        $('.message.confirmation').hide();
        $('.message.signup').show();
    });

    $('.overlay > a, .overlay .button').on('click', function () {
        $('.content_wrapper').removeClass('overlay_open');
        $('.overlay').removeClass('open').addClass('close');
        setTimeout(function(){
            $('.overlay').removeClass('close');
        }, 500);
        
    });
}

// TABLES (Selective)

/*  Modded by: Josh Holloran for Aruba Networks
    Author: Maggie Wachs, www.filamentgroup.com
    Date: November 2011
    Dependencies: jQuery, jQuery UI widget factory
*/


(function( $ ) {
  $.widget( "selective.table", { // need to come up with a better namespace var...
 
    options: {
      idprefix: null,   // specify a prefix for the id/headers values
      persist: null, // specify a class assigned to column headers (th) that should always be present; the script not create a checkbox for these columns
      checkContainer: null // container element where the hide/show checkboxes will be inserted; if none specified, the script creates a menu
    },
 
    // Set up the widget
    _create: function() {
      var self = this,
            o = self.options,
            table = self.element,
            thead = table.find("thead"),
            tbody = table.find("tbody"),
            hdrCols = thead.find("th"),
            bodyRows = tbody.find("tr"),
            container = o.checkContainer ? $(o.checkContainer) : $('.dropdown');
      
      // add class for scoping styles - cells should be hidden only when JS is on
      table.addClass("enhanced");
      
      hdrCols.each(function(i){
         var th = $(this),
               id = th.attr("id"),
               classes = th.attr("class");
         
         // assign an id to each header, if none is in the markup
         if (!id) {
            id = ( o.idprefix ? o.idprefix : "col-" ) + i;
            th.attr("id", id);
         }
         
         // assign matching "headers" attributes to the associated cells
         // TEMP - needs to be edited to accommodate colspans
         bodyRows.each(function(){
            var cell = $(this).find("th, td").eq(i);
            cell.attr("headers", id);
            if (classes) { cell.addClass(classes); }
         });
         
         // create the hide/show toggles
         if ( !th.is("." + o.persist) ) {
             var toggle = $('<li><input type="checkbox" name="toggle-cols" id="toggle-col-'+i+'" value="'+id+'" /> <label for="toggle-col-'+i+'">'+th.text()+'</label></li>');
             
             container.find("ul").append(toggle);
             
             toggle.find("input")
                .change(function(){
                   var input = $(this),
                      val = input.val(),
                      cols = $("#" + val + ", [headers="+ val +"]");
                   
                   if (input.is(":checked")) { cols.show(); }
                   else { cols.hide(); }
                })
                .bind("updateCheck", function(){
                   if ( th.css("display") === "table-cell" || th.css("display") === "inline" ) {
                      $(this).prop("checked", true);
                   }
                   else {
                      $(this).prop("checked", false);
                   }
                })
                .trigger("updateCheck");
            }
               
      }); // end hdrCols loop 
      
      // update the inputs' checked status
      $(window).bind("orientationchange resize", function(){
         container.find("input").trigger("updateCheck");
      });
              
    }, // end _create
    
   disable: function() {
        // TBD
    },

    enable: function() {
        // TBD
    }
    
  });
}( jQuery ) );

$(function(){ // on DOM ready

   $("#selective_1").table({
      idprefix: "co-",
      persist: "persist"
   });

});  // end DOM ready