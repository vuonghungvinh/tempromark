/*
Carousel application.
*/

/*jslint browser: true, indent: 4, maxlen: 80, plusplus: true, vars: true */
/*global $, console, jQuery,  */

(function () {
    "use strict";

    var current_position = [];
    var carousel_data = [];
    var visible_data = [];
    var auto_players = [];

    /*
    Get carousel container from supplied element
    HTMLelement
        Current HTMLelement
    return html element
        Container html div element
    */
    function getContainer(element) {
        var container;

        // If carousel container passed in return
        if ($(element).hasClass('carousel')) {
            return element;
        }

        container = $(element).parents(".carousel");
        if (container.length < 1) {
            console.warn('Carousel: Container not found.');
            return;
        }
        return container[0];
    }

    /*
    Get carousel stage element from supplied element
     html element
        Current element
    @return html element
        Stage html div element
    */
    function getStage(element) {
        var stage;

        stage = $(getContainer(element)).find(".carousel-stage");
        if (stage.length < 1) {
            console.warn('Carousel: Stage found.');
            return;
        }
        return stage[0];
    }

    /*
    Get carousel slider element from supplied element
    html element
        Current element
    return html element
        Slider html div element
    */
    function getSliders(element) {
        var sliders;

        sliders = $(getContainer(element)).find(".carousel-sliders a");
        if (sliders.length < 2) {
            console.warn('Carousel: Sliders not found.');
            return;
        }
        return sliders;
    }

    /*
    Get carousel data container
    html element
        Current element
    return html element
        Container html ol element
    */
    function getDataContainer(element) {
        var data_container;

        data_container = $(getContainer(element)).find(".carousel-stage ol");
        if (data_container.length < 1) {
            console.warn('Carousel: No Data Container found.');
            return;
        }
        return data_container[0];
    }

    /*
    Get carousel data elements
    HTMLelement
        Current HTMLelement
    return array
        Array of html li elements
    */
    function getData(element) {
        var data;

        data = $(getContainer(element)).find(".carousel-stage ol > li");
        if (data.length < 1) {
            console.warn('Carousel: No Data found.');
            return;
        }
        return data;
    }

    /*
    Get carousel navigation Container element
    html element
        Current element
    return html element
        Container html div element
    */
    function getNavigationContainer(element) {
        var nav_container;

        nav_container = $(getContainer(element)).find(".carousel-navigation");
        if (nav_container.length < 1) {
            console.warn('Carousel: Navigation Container not found.');
            return;
        }
        return nav_container[0];
    }

    /*
    Update the visable data based on the current carousel position.
     HTMLelement data_container
        HTML ol element
     int identifier
        Carousel Identifier
    */
    function updateData(data_container, identifier) {
        var clone, data, left_pos, right_pos, width, visible;

        visible = [];

        $(data_container).css('left', '-100%');
        data = $(carousel_data[identifier]).clone(true);
        if (data.length > 2) {
            $(getData(data_container)).remove(); // Remove current visible data

            // Tweak data ordering, show data for current and prev/next elements
            left_pos = current_position[identifier] - 1;
            if (left_pos < 0) {
                visible[0] = data[data.length - 1];
            } else {
                visible[0] = data[left_pos];
            }

            visible[1] = data[current_position[identifier]];

            right_pos = current_position[identifier] + 1;
            if (right_pos >= data.length) {
                visible[2] = data[0];
            } else {
                visible[2] = data[right_pos];
            }

            $(visible).prependTo(data_container); // Insert reordered data.
        }

        // If we only have 2 elements we need to clone one extra.
        if (data.length === 2) {
            $(getData(data_container)).remove(); // Remove current visible data

            visible[0] = data[current_position[identifier] - 1];
            visible[1] = data[current_position[identifier]];
            visible[2] = data[current_position[identifier] + 1];

            clone = $(data).clone(true);

            if (visible[0] === undefined) {
                visible[0] = clone[1];
            }

            if (visible[2] === undefined) {
                visible[2] = clone[0];
            }

            $(visible).prependTo(data_container); // Insert reordered data.
        }

        // If we have only one element show it and hide controls
        if (data.length === 1) {
            $(getDataContainer(data_container)).css('left', 0);
            $(getSliders(data_container)).hide();
            $(getNavigationContainer(data_container)).hide();

            $(getData(data_container)).remove(); // Remove current visible data
            visible[0] = data[current_position[identifier]];
            $(visible).prependTo(data_container); // Insert reordered data.
        }

        // Assign visible elements to global varible
        visible_data[identifier] = visible;
    }

    /*
    Get carousel navigation data elements from supplied element
    element
        Current element
    array
        Array of html li elements
    */
    function getNavigationData(element) {
        var navigation;

        navigation = $(getContainer(element)).find(".carousel-navigation li");
        if (navigation.length < 1) {
            console.warn('Carousel: Navigation Data not found.');
            return;
        }
        return navigation;
    }

    /*
    Update Navigation position based on the current carousel position.
    HTMLelement data_container
        HTML ol element
    int identifier
        Carousel Identifier
    */
    function updateNavigation(data_container, identifier) {
        var navigation;

        navigation = getNavigationData(data_container);

        if (navigation === undefined) {
            return;
        }

        $(navigation).removeClass('selected');
        $(navigation[current_position[identifier]]).addClass('selected');
    }

    /*
    Update the current postion based on left/right movement
     HTMLelement data_container
        HTML ol element
    int new_position
        New position to update carousel data
    int identifier
        Carousel Identifier
    */
    function update(data_container, new_position, identifier) {
        var data;

        data = carousel_data[identifier];
        current_position[identifier] = new_position;
        if (current_position[identifier] > data.length - 1) {
            current_position[identifier] = 0;
        }

        if (current_position[identifier] < 0) {
            current_position[identifier] = data.length - 1;
        }

        // Update the visable data on the page.
        updateData(data_container, identifier);
        updateNavigation(data_container, identifier);
        updateSliders(data_container, identifier);
    }

    /*
    Update thumbnail images in left/right sliders.
    */
    function updateSliders(data_container, identifier) {
        var data, left_image, right_image, sliders, slider_thumb;

        data = visible_data[identifier];
        left_image = $(data[0]).attr('data-thumbnail');
        right_image = $(data[2]).attr('data-thumbnail');

        if(! left_image && ! right_image) {
            return false;
        }


        sliders = getSliders(data_container);
        slider_thumb = $(sliders[0]).find('img')[0];
        if(slider_thumb) {
            slider_thumb.src = left_image;
        } else {
            sliders[0].innerHTML = '<img src="' + left_image + '" />' +
                sliders[0].innerHTML;
        }

        slider_thumb = $(sliders[1]).find('img')[0];
        if(slider_thumb) {
            slider_thumb.src = right_image;
        } else {
            sliders[1].innerHTML = '<img src="' + right_image + '" />' +
                sliders[1].innerHTML;
        }
    }

    /*
    Preform slide animation
    */
    function slideAnimation(action, new_position, data_container, identifier, elem) {
        var move, position, width, x;

        position = parseInt($(data_container).css('left'), 10);
        width = parseInt($(getStage(data_container)).css('width'), 10);

        if (action === 'slide-left') {
            move = '0%';
        }

        if (action === 'slide-right') {
            move = '-200%';
        }

        $(data_container).animate({"left": move}, 1000, "swing",
            function () { update(data_container, new_position, identifier);
                $(elem).unbind('click');
                $(elem).click(slideEvent);
            });
    }

    /*
    Prep for slide left/right animation.
    */
    function slide(action, identifier, data_container, elem) {
        var new_position;

        if (action === 'slide-left') {
            new_position = current_position[identifier] - 1;
        }

        if (action === 'slide-right') {
            new_position = current_position[identifier] + 1;
        }

        slideAnimation(action, new_position, data_container, identifier, elem);
        return false;
    }

    /*
    Autoplay for carousel
    carousel
        HTML elemeent for main wrapper 'carousel' div
    int identifier
        Unique integer identifier
    */
    function autoplayCarousel(carousel, identifier) {
        var auto_play, data, data_container, stage, time;

        stage = getStage(carousel);
        data = getData(carousel);
        auto_play = $(stage).attr('data-autoplay');
        if (auto_play === 'true' && data.length > 1) {
            time = parseInt($(stage).attr('data-time'), 10);
            data_container = getDataContainer(carousel);
            auto_players[identifier] = setInterval(function () { slide('slide-right', identifier, data_container); }, time);
        }
    }

    /*
    Decorate html elements within carousel.
    carousel
        HTML elemeent for main wrapper 'carousel' div
    int identifier
        Unique integer identifier
    */
    function decorate(carousel, identifier) {
        var class_selected, data, nav_container, nav_data, stage, x;

        stage = getStage(carousel);
        $(stage).attr('data-identifier', identifier);

        data = getData(carousel);
        carousel_data[identifier] = $(data).clone(true);

        nav_data = '';
        for (x = 0; data.length > x; x++) {
            class_selected = '';
            if (data[x].className === 'carousel-selected') {
                class_selected = 'class="selected"';
            }

            // Build navigation elements
            nav_data += '<li ' + class_selected +
                '><a href="" data-identifier="' + identifier +
                '" data-target="' + x + '">' + '</a></li>';
        }

        // Print Navigation Elements if container found.
        nav_container = getNavigationContainer(carousel);
        if (typeof (nav_container) !== 'undefined') {
            $('<ol>' + nav_data + '</ol>').prependTo(nav_container);
        }
    }

    /*
    Slider button click event
    */
    function slideEvent(event) {
        var action, data_container, elem, identifier;

        elem = event.target;
        if(elem.tagName !== 'A') {
            elem = $(event.target).parent();
        }

        action = $(elem).attr('data-action');
        identifier = $(elem).attr('data-identifier');
        data_container = getDataContainer(elem);

        clearInterval(auto_players[identifier]); // Clear autoplay

        $(elem).unbind('click');
        $(elem).click(function(){ return false; });
        slide(action, identifier, data_container, elem);
        return false;
    }

    /*
    Navigate to particular position in the carousel
    */
    function navigate(event) {
        var action, clone_data, data_container, elem, identifier, target;

        elem = event.target;
        target = parseInt($(elem).attr('data-target'), 10);
        identifier = $(elem).attr('data-identifier');

        if (target < current_position[identifier]) {
            action = 'slide-left';
            visible_data[identifier][0] = carousel_data[identifier][target];
        }

        if (target > current_position[identifier]) {
            action = 'slide-right';
            visible_data[identifier][2] = carousel_data[identifier][target];
        }

        // Remove current visible data
        data_container = getDataContainer(elem);
        $(getData(data_container)).remove();

        // Clone then Instert reordered Data
        // *NOTE* We must clone data to ensure we have unique HTML elements.
        clone_data = $(visible_data[identifier]).clone();
        $(clone_data).prependTo(data_container);

        if (action !== undefined) {
            slideAnimation(action, target, data_container, identifier);
        }

        clearInterval(auto_players[identifier]); // Clear autoplay

        return false;
    }

    function swipe(event) {
        var action, data_container, elem, identifier, stage, swipe;

        elem = event.target;
        stage = getStage(elem);
        identifier = $(stage).attr('data-identifier');
        data_container = getDataContainer(stage);

        // determine swipe direction
        swipe = event.type;
        if (swipe === 'swiperight') {
            action = 'slide-left'
        }

        if (swipe === 'swipeleft') {
            action = 'slide-right'
        }

        slide(action, identifier, data_container, undefined);
    }


    /*
    Setup event handlers
    HTMLelement carousel
        html div element
    int identifier
        Carousel Identifier
    */
    function events(carousel, identifier) {
        var navigation, sliders, stage;

        stage = getStage(carousel);
        $(stage).on('swipeleft', swipe);
        $(stage).on('swiperight', swipe);

        sliders = getSliders(carousel);
        $(sliders).click(slideEvent);
        $(sliders).attr('data-identifier', identifier);

        navigation = getNavigationData(carousel);
        $(navigation).find('a').click(navigate);
    }

    /*
    Set carousel stage and element width/height
    element carousel
        html div element
    int identifier
        Carousel Identifier
    */
    function setDimensions(carousel, identifier) {
        var data, stage;

        // Set carousel elements width and height
        data = carousel_data[identifier];
        data.width('33.3333%');
        data.height('100%');

        // Set max requried carousel width
        stage = getStage(carousel);
        $(stage).children('ol').width('300%');
    }


    /*
    Set Carousel Starting position.
     - Sets the starting position too the li element with a class of selected.
     - Defaults to the first li element if no start position specified.
    element carousel
        html div element
    int identifier
        Carousel Identifier
    */
    function setStartPosition(carousel, identifier) {
        var data, data_container, item, x;

        current_position[identifier] = 0;
        data = carousel_data[identifier];
        for (x = 0; data.length > x; x++) {
            item = data[x];
            if (item.className === 'carousel-selected') {
                current_position[identifier] = x;
            }
        }

        data_container = getDataContainer(carousel);
        updateData(data_container, identifier);
        updateSliders(data_container, identifier);
        updateNavigation(data_container, identifier);
    }

    function init() {
        var carousels, x;

        carousels = $(".carousel");
        for (x = 0; carousels.length > x; x++) {
            decorate(carousels[x], x);
            setDimensions(carousels[x], x);
            setStartPosition(carousels[x], x);
            events(carousels[x], x);
            autoplayCarousel(carousels[x], x);
        }
    }

    jQuery(init);

}());
