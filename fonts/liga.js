/* Add the class "noliga" to the html element if browser doesn't support font-feature-settings */

$(document).ready(function() {
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
});