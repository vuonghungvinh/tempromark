
/*jslint browser: true, indent: 4, maxlen: 80, plusplus: true, vars: true */
/*global $, console, jQuery,  */

(function () {
    "use strict";

    /*
    Setup event handlers
    HTMLelement slider_viewer
        html div element
    int identifier
        slide_viewer Identifier
    */
    function events(slide_viewer, identifier) {
        var controls;

        controls = getControls(slide_viewer);
        $(controls).click(slideEvent);
        $(controls).attr('data-identifier', identifier);
    }


    /*
    Get control elements from supplied element
    html element
        Current element
    return html elements
        Control html a elements
    */
    function getControls(element) {
        var controls;

        controls = $(getContainer(element)).find(".slide-viewer-controls a");
        if (controls.length < 2) {
            console.warn('Slide Viewer: Controls not found.');
            return;
        }
        return controls;
    }

    /*
    Preform slide animation
    */
    function slideAnimation(action, identifier, data_container, element) {
        var current_position, elements, height, max_position, move, stage;

        current_position = parseInt($(data_container).css('top'), 10);
        stage = getStage(data_container);
        height = parseInt($(stage).css('height'), 10);

        elements = $(data_container).find('li');
        if (action === 'slide-down') {
            move = current_position - height;
            max_position = parseInt(0 - elements.length * height, 10)
            if (move <= max_position )
                move = current_position;
        }

        if (action === 'slide-up') {
            move = current_position + height;
            if (move > 0) {
                move = 0;
            }
        }

        $(data_container).animate({"top": move}, 1000, "swing",
            function () {
                $(element).unbind('click');
                $(element).click(slideEvent);
            });
    }

    /*
    Slider button click event
    */
    function slideEvent(event) {
        var action, data_container, element, identifier;

        element = event.target;
        if(element.tagName !== 'A') {
            element = $(event.target).parent();
        }

        action = $(element).attr('data-action');
        identifier = $(element).attr('data-identifier');
        data_container = getDataContainer(element);

        $(element).unbind('click');
        $(element).click(function(){ return false; });
        slideAnimation(action, identifier, data_container, element);
        return false;
    }

    /*
    Get container from supplied element
    HTMLelement
        Current HTMLelement
    return html element
        Container html div element
    */
    function getContainer(element) {
        var container;

        // If slide viewer container passed in return
        if ($(element).hasClass('slide-viewer')) {
            return element;
        }

        container = $(element).parents(".slide-viewer");
        if (container.length < 1) {
            console.warn('Slide Viewer: Container not found.');
            return;
        }
        return container[0];
    }

    /*
    Get data container
    html element
        Current element
    return html element
        html ul element
    */
    function getDataContainer(element) {
        var data_container;

        data_container = $(getContainer(element)).find(".slide-viewer-stage ul");
        if (data_container.length < 1) {
            console.warn('Slide Viewer: No Data Container found.');
            return;
        }
        return data_container[0];
    }

    function getStage(element) {
        var stage

        stage = $(getContainer(element)).find(".slide-viewer-stage");
        if (stage.length < 1) {
            console.warn('Slide Stage: Stage not found.');
            return;
        }
        return stage[0];

    }

    function init() {
        var slide_viewers, x;

        slide_viewers = $(".slide-viewer");
        for (x = 0; slide_viewers.length > x; x++) {
            events(slide_viewers[x], x);
        }
    }



    jQuery(init);

}());
