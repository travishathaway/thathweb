(function( $ ) {
    $.fn.oepager = function( options ) {
        // This will come in handy later, no pun intended ;)
        var self = this;
        // Unix timestamp of last key up event
        var last_keyup = 0;
        // Default settings for our plugin
        var defaults = {
            // How fast the search bar checks for
            // user input
            responsiveness : 100,
            // This function is call after results
            // have been loaded
            callback : undefined,
            // Where we get paged results
            pager_url : '',
            // Whether or not to use the search-as-you-type
            autosearch : true
        }
        // These are non-form elements we pass to the search
        var extra_params = {};

        var settings = $.extend( {}, defaults, options);

        // Order by controls
        this.on('click', '.order-by', function(e){
            var column = $(this).data('order-by');

            if( extra_params.order_by === undefined ){
                extra_params.order_by = column;
            }

            if( extra_params.order_by.indexOf('-') == -1 ) {
                if( extra_params.order_by == $(this).data('order-by') ){
                    extra_params.order_by = '-' + $(this).data('order-by');
                } else {
                    extra_params.order_by = $(this).data('order-by');
                }
            } else {
                extra_params.order_by = '';
            }

            updateResults(self, settings, extra_params);
        });

        // Paginator Controls
        this.on('click', '.page-number', function(){
            extra_params.page = $(this).data('page-number');
            updateResults(self, settings, extra_params);
            
            if( settings.animate ){
                $("html, body").animate({ scrollTop: 0 }, "slow");
            }
        });

        // Ajax controls this form
        $('form.oepager').on('submit', function(e){
            e.preventDefault();
        });

        // Auto Search text
        if( settings.autosearch ){
            $('form.oepager input[type="text"]').on('keyup', function(){
                // responsiveness is how we control the responsiveness of the auto search
                // more is less ;) 
                var cur_keyup = Date.now();

                if( (cur_keyup - last_keyup) > settings.responsiveness ) {
                    updateResults(self, settings, extra_params);
                }
                last_keyup = cur_keyup;
            });
        } else {
            // Input text
            $('form.oepager input[type="text"]').on('keydown', function(e){
                if( e.keyCode == 13 ) {
                    extra_params.page = 1;
                    updateResults(self, settings, extra_params);
                }
            });
        }

        // Select box changes
        $('form.oepager select').on('change', function(){
            extra_params.page = 1;
            updateResults(self, settings, extra_params);
        });

        // Input checkboxes change
        $('form.oepager input[type="checkbox"]').on('change', function(){
            extra_params.page = 1;
            updateResults(self, settings, extra_params);
        });

        // Input radio change
        $('form.oepager input[type="radio"]').on('change', function(){
            extra_params.page = 1;
            updateResults(self, settings, extra_params);
        });

        // Search button
        $('form.oepager button').on('click', function(){
            extra_params.page = 1;
            updateResults(self, settings, extra_params);
        });

        // Listens for an event telling it to refresh page results
        this.on('oepage.updateResults', function(){
            updateResults(self, settings, extra_params);
        });

        $(window).hashchange( function(){
            getResults(self, settings);
        });

        getResults(self, settings);

        return this;
    }

    function updateResults(self, settings, extra_params){
        // Build our search string
        search_string = $.param(extra_params);
        search_string += '&' + $('form.oepager').serialize()

        location.hash = search_string;
        $('.page-number').attr('href', location.hash);
        $('.order-by').attr('href', location.hash);
        $(window).hashchange();
    }

    function updateFormValues(search_string){
        /* 
         * This function updates all form elements under form.oepager
         * and handles the following form types:
         *     - select
         *     - select[multiple="multiple"]
         *     - input[type="radio"]
         *     - input[type="checkbox"]
         *     - input[type="text"]
         */

        qs_obj = $.deparam(search_string);

        $.each(qs_obj, function(key, value){
            form_elm = $('form.oepager [name="'+key+'"]');
            if( !$.isEmptyObject(form_elm) ){
                // see if it's a select
                if( form_elm.is('select') ){
                    // are we dealing with multiple values in a multiple select?
                    if( form_elm.attr('multiple') == 'multiple' && typeof(value) != 'string' ){
                        $.each(value, function(key, f_value){
                            console.log(f_value);
                            form_elm.children(
                                'option[value="'+f_value+'"]'
                            ).attr('selected', true);
                        });
                    // Works for both multiple select with single value and single select
                    } else {
                        form_elm.children(
                            'option[value="'+value+'"]'
                        ).attr('selected', true);
                    }
                } else if( form_elm.is('input[type="text"]') ){
                    form_elm.val(value);
                } else if( form_elm.is('input[type="radio"], input[type="checkbox"]') ){
                    $.each(form_elm, function(f_key, f_elm){
                        if( f_elm.value == value ){
                            f_elm.checked = true;
                        }
                    })
                }
            }
        });

        try {
            // not all pages have chosen on them
            $('.chosen').trigger('chosen:updated');
        } catch(error) {
            // Do nothing
        }
    }

    function getResults(self, settings){
        // Show the loading gif
        $('form.oepager .loading').removeClass('hide');
        $('#search-loading-results').removeClass('hide');

        search_string = location.hash.replace('#','');

        updateFormValues(search_string);

        search_string += '&partial=1';

        $.get(settings.url, search_string, function(data) {
            $('form.oepager .loading').addClass('hide');
            $('#search-loading-results').addClass('hide');
            self.html(data);

            if ( settings.callback != undefined ) {
                settings.callback();
            }
        });
    }

}( jQuery ));
