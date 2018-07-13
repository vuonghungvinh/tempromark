/*
Gallery application.
*/

/*jslint browser: true, indent: 4, maxlen: 80, plusplus: true, vars: true */
/*global $, console, jQuery,  */

(function () {
    "use strict";

    /*
    Setup galley stage with first slide & gallery page controls
    */
    function decorate(gallery) {
        var data_container, caption_button, caption_state, caption_alt, first,
        pages, stage, thumbnails, thumb_limit;

        data_container = getDataContainer(gallery);

        // Set First Slide
        first = $(data_container).find('.gallery-slide').clone()[0];
        stage = getStage(gallery);
        $(first).prependTo(stage);

        // Hide caption button if no caption for first slide.
        if( $(first).find('.gallery-caption').length > 0 ) {
            $(stage).find('.gallery-caption-toggle').fadeIn('slow');
        }
        else {
            $(stage).find('.gallery-caption-toggle').hide();
        }

        // Caption toggle state
        caption_state = $(data_container).attr('data-caption-state');
        if(caption_state === 'closed') {
            caption_button = $('.gallery-caption-toggle');
            caption_alt = caption_button.attr('data-alt-text');
            caption_button.attr('data-alt-text', caption_button[0].textContent);
            caption_button[0].textContent = caption_alt;
            $('.gallery-caption').hide();
        }

        // Add 'selected' class to first thumbnail
        thumbnails = getThumbnails(gallery);
        $(thumbnails[0]).addClass('selected');

        // Determine number of thumbnails per page
        thumb_limit = parseInt(
            $(getDataContainer(gallery)).attr('data-page-limit'), 10);

        updateThumbnails(1, thumbnails, thumb_limit);

        // Default to showing all images if limit not specified.
        if (isNaN(thumb_limit)) {
            thumb_limit = thumbnails.length;
            console.info(
                'Gallery: Page Limit not defined, showing all images.'
            );
        }

        insertPageNavigation(gallery, thumbnails.length, thumb_limit);
    }

    /*
    Setup event handers.
    */
    function eventSetup() {
        $('.gallery-thumbnail').click(showSlide);
        $('.gallery-caption-toggle').click(toggleCaption);
        $('.gallery-pages a.gallery-page').click(showGalleryPage);
        $('a.gallery-page-next, a.gallery-page-prev').click(slideGalleryPage);
    }

    /*
    Get gallery container from supplied element
    @param HTMLelement element
        Current html element
    @return HTMLelement
        Container html div element
    */
    function getContainer(element) {
        var container;

        // If gallery container passed in return it
        if (element.className === 'gallery') {
            return element;
        }

        container = $(element).parents(".gallery");
        if (container.length < 1) {
            console.warn('Gallery: Container not found.');
            return;
        }
        return container[0];
    }

    /*
    Get gallery caption container from supplied element
    @param HTMLelement element
        Current html element
    @return HTMLelement
        Caption container html div element
    */
    function getCaptionContainer(element) {
        var container;

        container = $(getContainer(element)).find(".gallery-caption");
        if (container.length < 1) {
            console.warn('Gallery: Caption Container not found.');
            return;
        }
        return container[0];
    }

    /*
    Get gallery data container from supplied element
    @param HTMLelement element
        Current html element
    @return HTMLelement
        Data container - html ul element
    */
    function getDataContainer(element) {
        var container;

        container = $(getContainer(element)).find('.gallery-data');
        if (container.length < 1) {
            console.warn('Gallery: Data Container not found.');
            return;
        }
        return container[0];
    }

    /*
    Get page navigation from supplied element
    @param HTMLelement element
        Current html element
    @return HTMLelement
        Container html div element
    */
    function getNavigationContainer(element) {
        var container;

        container = $(getContainer(element)).find('.gallery-pages');
        if (container.length < 1) {
            console.warn('Gallery: Navigation Container not found.');
            return;
        }
        return container[0];
    }

    /*
    Get gallery Stage from supplied Element
    @param HTMLelement element
        Current html element
    @return HTMLelement
        Stage html div element
    */
    function getStage(element) {
        var stage;

        stage = $(getContainer(element)).find(".gallery-stage");
        if (stage.length < 1) {
            console.warn('Gallery: Stage not found.');
            return;
        }
        return stage[0];
    }

    /*
    Get list of gallery thumbnails from supplied element
    @param HTMLelement element
        Current html element
    @return array
        Array of html anchor elements
    */
    function getThumbnails(element) {
        var thumbnails;

        thumbnails = $(getDataContainer(element)).find('.gallery-thumbnail');
        if (thumbnails.length < 1) {
            console.warn('Gallery: Thumbnails not found.');
            return;
        }
        return thumbnails;
    }

    /*
    Insert Thumbnail page navigation.
    @param HTMLelement gallery
        html div element
    @param number total_thumbs (Integer)
        Number of thumbnails in gallery
    @param number limit (Integer)
        Number of thumbnails to display per page.
    */
    function insertPageNavigation(gallery, total_thumbs, limit) {
        var class_name, nav_elements, navigation_container, pages, x;

        pages = Math.ceil(total_thumbs / limit);

        // Don't insert page navigation if only one page of thumbnails
        if (pages < 2) {
            return;
        }

        nav_elements = '<li>' +
            '<a class="gallery-page-prev" href="#">&lsaquo;</a></li>';

        // Default first page as selected
        class_name = 'selected';
        for (x = 1; x <= pages; x++) {
            if (x > 1) {
                class_name = '';
            }
            nav_elements += '<li><a id="gallery-page-' +
                x + '" class="gallery-page ' +
                class_name + '" href="#" data-page="' +
                x + '">' + x + '</a></li>';
        }

        nav_elements += '<li>' +
            '<a class="gallery-page-next" href="#">&rsaquo;</a></li>';

        navigation_container = getNavigationContainer(gallery);
        $('<ul>' + nav_elements + '</ul>').prependTo(navigation_container);
    }

    /*
    Update/replace main gallery stage when a thumbnail is clicked.
    */
    function showSlide(event) {
        var element;

        element = event.target;
        updateSlide(element);

        // Update 'selected' class for thumbnails
        $(getThumbnails(element)).removeClass('selected');
        $(element).addClass('selected');

        return false;
    }

    /*
    Show Gallery Page Event. Prepares Gallery page data for new thumbnails.
    */
    function showGalleryPage(event) {
        var current_page, limit, thumbnails;

        current_page = parseInt($(event.target).attr('data-page'), 10);
        thumbnails = getThumbnails(event.target);
        limit = $(getDataContainer(event.target)).attr('data-page-limit');
        updateThumbnails(current_page, thumbnails, limit);

        // Update 'selected' class for page navigation
        $(getNavigationContainer(event.target)).find('a.gallery-page').
            removeClass('selected');

        $(event.target).addClass('selected');
        return false;
    }

    /*
    Prev/Next Page Event
    */
    function slideGalleryPage(event) {
        var current_page, next_page;

        current_page = $('.gallery-page.selected');

        // Next...
        if (event.target.className === 'gallery-page-next') {
            next_page = $(current_page).parent().next().
                children('a.gallery-page');

            // Loop to start if last element reached
            if (next_page.length < 1) {
                next_page = $(current_page).parent().siblings().
                    children('a.gallery-page').first();
            }
        }

        // Prev...
        if (event.target.className === 'gallery-page-prev') {
            next_page = $(current_page).parent().prev().
                children('a.gallery-page');

            // Loop to end if first element reached
            if (next_page.length < 1) {
                next_page = $(current_page).parent().siblings().
                    children('a.gallery-page').last();
            }
        }

        next_page.click();
        return false;
    }

    /*
    Toggle Caption visibility & cycle button symbol
    */
    function toggleCaption(event) {
        var button, caption, caption_alt, caption_button, caption_state,
            data_container, symbol, symbol_alt;

        caption = $(getCaptionContainer(event.target));
        if($(caption).queue('fx').length < 1) {
            caption.fadeToggle(500);
        }

        // Cycle caption symbol
        caption_button = $(getStage(event.target)).find('.gallery-caption-toggle')[0];
        caption_alt = $(caption_button).attr('data-alt-text');
        $(caption_button).attr('data-alt-text', caption_button.textContent);
        caption_button.textContent = caption_alt;

        // Record caption state
        data_container = getDataContainer(event.target);
        caption_state = $(data_container).attr('data-caption-state');
        if(caption_state === 'open') {
            $(data_container).attr('data-caption-state', 'closed')
        }
        else {
            $(data_container).attr('data-caption-state', 'open')
        }

        return false;
    }

    /*
    Update Stage with new Slide
    @param HTMLelement element
        html anchor element
    */
    function updateSlide(element) {
        var caption, caption_button, caption_state, current_slide, new_slide;

        current_slide = $(getStage(element)).find('.gallery-slide')[0];

        // Insert new slide into stage
        new_slide = $(element).parent().find('.gallery-slide').clone();
        $(new_slide).insertBefore(current_slide);

        // Fade out and remove current slide, revealing the new
        $(current_slide).fadeOut('slow',
            function () { $(current_slide).remove(); });

        // Slide caption state
        caption_button = $(getStage(element)).find('.gallery-caption-toggle');
        caption = $(new_slide).find('.gallery-caption')
        caption_state = $(getDataContainer(element)).attr('data-caption-state')
        if(caption.length > 0) {
            caption_button.fadeIn('slow');
            if(caption_state === 'open') {
                caption.fadeIn('slow');
            }
        }
        else {
            // Hide caption & button if no caption for new slide.
            caption_button.fadeOut('slow');
            caption.fadeOut('slow');
        }
    }

    /*
    Set visible thumbnails based on current page position and thumbnail
    limit per page.
    @param number current_page (Integer)
        Current Page being viewed.
    @param array thumbnails
        Array of html anchor elements
    @parma number limit (Integer)
        Number of thumnails visable per page.
    */
    function updateThumbnails(current_page, thumbnails, limit) {
        var end, hide, show, start, x;

        // Calculate range of viewable thumbnails
        start = (limit * current_page) - limit;
        end = start + (limit - 1);

        show = [];
        hide = [];
        for (x = 0; x < thumbnails.length; x++) {
            if (x >= start && x <= end) {
                show.push(thumbnails[x]);
            } else {
                hide.push(thumbnails[x]);
            }
        }

        $(hide).hide();
        $(show).show();
    }

    function init() {
        var galleries, x;

        galleries = $('.gallery');
        for (x = 0; x < galleries.length; x++) {
            decorate(galleries[x]);
        }

        eventSetup(); // Event Handlers
    }

    jQuery(init);

}());
