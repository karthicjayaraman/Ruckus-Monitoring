$(document).ready(function() {

    //PREVENT PAGE JUMPS WHEN CLICKING EMPTY LINKS
    $('a[href="#"]').click(function (e) {
        e.preventDefault();
    });

    //HIGHLIGHT.JS
    $('pre code').each(function(i, e){hljs.highlightBlock(e);});
    $('code').click(function() {$(this).selectText();});

    //CALL FUNCTIONS FROM SCRIPTS.JS
    offcanvas();
    tabs();
    $('.responsive .tabcontrols').tinyNav();
    pills();
    dropdowns();
    alerts();
    overlay();

    //TOOLTIPS
    $('.tttop').tooltipster({
        interactive: 'true',
        maxWidth: '250',
        animation: 'grow',
        offsetY: '10'
    });
    $('.ttbottom').tooltipster({
        interactive: 'true',
        maxWidth: '250',
        animation: 'grow',
        position: 'bottom',
        offsetY: '10'
    });
    $('.ttleft').tooltipster({
        interactive: 'true',
        maxWidth: '250',
        animation: 'grow',
        position: 'left',
        offsetX: '10'
    });
    $('.ttright').tooltipster({
        interactive: 'true',
        maxWidth: '250',
        animation: 'grow',
        position: 'right',
        offsetX: '10'
    });

    //ICON FONT FALLBACK
    if (!$('html').hasClass('fontface')) {
        $('[class*="icon_"]').iconfontFallback();
    }

    //TABLES (SELECTIVE)

    $(function(){ // on DOM ready

       $("#selective_1").table({
          idprefix: "co-",
          persist: "persist"
       });

    });

    //SELECT 2

    $('.select2').select2({
        // Add our 'needsclick' to each item, so FastClick doesn't get applied
        formatResult: function(result, container, query, escapeMarkup) {
            container.addClass('needsclick');
            return result.text;
        }
    });

});