/*
Install Redactor
*/

/*jslint browser: true, indent: 4, maxlen: 80, plusplus: true, vars: true */
/*global $, console, jQuery,  */

(function () {
    "use strict";

    function init() {
        var elements, custom_settings, default_settings, settings, x;

        elements = $('.redactor');
        for(x = 0; x < elements.length; x++) {
            custom_settings = $(elements[x]).attr('data-settings');
            if(custom_settings) {
                custom_settings = $.parseJSON(custom_settings);
            }

            default_settings = {
                buttonsAdd: ['|', 'special_characters', '|'],
                buttonsCustom: {
                    special_characters: {
                        title: 'Special Characters',
                        dropdown: {
                            copyright: {
                                title: 'Copyright: &copy;',
                                callback: function(obj){
                                    obj.insertHtml('&copy;');
                                    }
                            },
                            registered: {
                                title: 'Registered: &reg;',
                                callback: function(obj){
                                    obj.insertHtml('&reg;');
                                }
                            },
                            trade_mark: {
                                title: 'Trade Mark: &trade;',
                                callback: function(obj){
                                    obj.insertHtml('&trade;');
                                }
                            },
                            ampersand: {
                                title: 'Ampersand: &amp;',
                                callback: function(obj){
                                    obj.insertHtml('&amp;');
                                }
                            },
                            degree: {
                                title: 'Degrees: &deg;',
                                callback: function(obj){
                                    obj.insertHtml('&deg;');
                                }
                            },
                            squared: {
                                title: 'Squared: &sup2;',
                                callback: function(obj){
                                    obj.insertHtml('&sup2;');
                                }
                            },
                            cubed: {
                                title: 'Cubed: &sup3;',
                                callback: function(obj){
                                    obj.insertHtml('&sup3;');
                                }
                            },
                            euro: {
                                title: 'Euro: &euro;',
                                callback: function(obj){
                                    obj.insertHtml('&euro;');
                                }
                            },
                            pound: {
                                title: 'Pound: &pound;',
                                callback: function(obj){
                                    obj.insertHtml('&pound;');
                                }
                            },
                            quater: {
                                title: '&frac14;',
                                callback: function(obj){
                                    obj.insertHtml('&frac14;');
                                }
                            },
                            half: {
                                title: '&frac12;',
                                callback: function(obj){
                                    obj.insertHtml('&frac12;');
                                }
                            },
                            three_quaters: {
                                title: '&frac34;',
                                callback: function(obj){
                                    obj.insertHtml('&frac34;');
                                }
                            },
                        }
                    }
                },
                formattingTags: ['p', 'blockquote', 'h1', 'h2', 'h3', 'h4'],
            }

            settings = $.extend(default_settings, custom_settings);
            $(elements[x]).redactor(settings);
        }
    }

    jQuery(init);

}());
