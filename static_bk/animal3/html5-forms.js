/**
Implement HTML5 form behaviours for browsers *cough*IE*cough* that don't
support them.  Requires the jQuery library.

@author    Leon Matthews <leon@lost.co.nz>
@copyright Copyright 2011-2012 Leon Matthews. All rights reserved.
@link      http://www.lost.co.nz/
@license   GPL
*/

/*jslint browser: true, indent: 4, maxlen: 80 */
/*global $, console, jQuery */

/**
HTML5 autofocus
*/
(function () {
    "use strict";

    // Initialise
    function init() {

        var elem, found = false, i, inputs;
        inputs = $(':input');
        for (i = 0; i < inputs.length; i++) {
            elem = $(inputs[i]);
            if (elem.prop('autofocus') !== undefined) {
                elem.focus();
                found = true;
                break;
            }
        }

        if (found) {
            console.log("Form autofocus: Focus placed on first input");
        } else {
            console.log("Form autofocus: No inputs found");
        }
    }

    jQuery(init);

}());


/**
HTML5 placeholder
*/
(function () {
    "use strict";

    // Show placeholder only if no form input is empty
    function show() {
        var placeholder = $(this).attr('placeholder');
        if (this.value.match('^\s*$')) {
            $(this).addClass('placeholder');
            this.value = placeholder;
        }
    }

    // Hide placeholder text
    function hide() {
        var placeholder = $(this).attr('placeholder');
        if (this.value === placeholder) {
            $(this).removeClass('placeholder');
            this.value = '';
        }
    }

    // Hide placeholder text in all inputs
    function hide_all() {
        $(':input[placeholder]').each(hide);
    }

    // Initialise
    function init() {

        // Find inputs with placeholder attributes
        var inputs = $(':input[placeholder]');
        console.log('Form placeholder: ' + inputs.length + " inputs found");

        // Install event handlers
        inputs.focusin(hide).focusout(show);

        // Clear placeholders when form submitted
        $('form').submit(hide_all);

        // Show placeholder initially
        inputs.each(show);
    }

    jQuery(init);

}());
