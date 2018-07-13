/**
JavaScript to complement Messiah Studio coding idioms.
*/

/*jslint browser: true, indent: 4, maxlen: 80 */
/*global $, console, jQuery, window */


/**
Provide safe fall-back for console object calls
*/
(function () {
    "use strict";

    if (typeof console === 'undefined') {
        var do_nothing, i, len, names;
        names = [
            'log', 'debug', 'info', 'warn', 'error',
            'assert', 'dir', 'dirxml', 'group', 'groupEnd',
            'time', 'timeEnd', 'count', 'trace', 'profile', 'profileEnd'
        ];
        window.console = {};
        do_nothing = function () {};
        for (i = 0, len = names.length; i < len; i += 1) {
            window.console[names[i]] = do_nothing;
        }
    }
}());


/**
Click-to-hide Django messages.
*/
(function () {
    "use strict";

    jQuery(function () {
        $('div.message').click(function () {
            $(this).slideUp();
        });
    });
}());


/**
Navigation highlighting.

Apply the class 'selected' to any links within navigation elements.  Use the
ALLOW_PREFIX constant to toggle between prefix and exact matching of link
paths.
*/
(function () {
    "use strict";

    var ALLOW_PREFIX = true;

    function check_link(link, is_selected) {
        var link_path, current_path;

        link_path = link.pathname;
        current_path = window.location.pathname;

        // Special case for homepage
        if (link_path === '/') {
            if (current_path === '/') {
                $(link).addClass('selected');
            }
        } else {
            if (is_selected(link_path, current_path)) {
                $(link).addClass('selected');
            }
        }
    }

    function is_match(a, b) {
        return (a === b) ? true : false;
    }

    function is_prefix(a, b) {
        var index = b.indexOf(a);
        return (index === 0) ? true : false;
    }

    function init() {
        var is_selected = ALLOW_PREFIX ? is_prefix : is_match;
        $('nav a').each(function () {
            check_link(this, is_selected);
        });
    }

    jQuery(init);

}());
