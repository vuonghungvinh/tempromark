/*
Popup box.
*/

/*jslint browser: true, indent: 4, maxlen: 80, plusplus: true, vars: true */
/*global $, console, jQuery,  */

(function () {
    "use strict";

    function open(event) {
        var element, target;

        element = event.target;
        if (element.tagName !== 'A') {
            element = $(event.target).parent();
        }

        target = $(element).attr('data-target');
        target = $('#'+target);
        $(target).removeClass('hidden');
        return false;
    }

    function close(event) {
        var element;

        element = event.target;
        if (element.tagName !== 'A') {
            element = $(event.target).parent();
        }

        $(element).parents('.popup').addClass('hidden');
        return false;
    }

    function init() {

        $("a.popup-open").click(open);
        $("a.popup-close").click(close);
    }

    jQuery(init);

}());
