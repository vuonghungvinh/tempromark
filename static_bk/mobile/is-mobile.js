
/*jslint browser: true, indent: 4, maxlen: 80, plusplus: true, vars: true */
/*global $, console, jQuery,  */

(function () {
    "use strict";

    function init() {
        if ('ontouchstart' in window) {
            $('#main-nav').addClass('mobile-device');
            setupTapEvents();
        }
    }

    function setupTapEvents() {
        var nav_elements, x, next;

        $('nav.mobile-device > ul ul').hide();
        nav_elements = $('nav.mobile-device > ul > li > a');
        for (x = 0; x < nav_elements.length; x++) {
            next = $(nav_elements[x]).next();
            if (next.length > 0) {
                $(nav_elements[x]).bind( "tap", tapHandler );
            }
        }
    }

    function tapHandler(event) {
        var hidden_nav;

        // Hide all open nav elements
        $('nav.mobile-device > ul ul').hide();

        // Bind tap events
        setupTapEvents();

        // Remove tap event from current element.
        $(event.target).unbind("tap");

        // Show hidden nav elements
        hidden_nav = $(event.target).next();
        $(hidden_nav).slideDown();
        return false;
    }


    jQuery(init);

}());
