jQuery(document).ready(function($){
    $(document).on('click', '.btn-user-id', function () {
        let userId = $(this).data('user-id');
        let url = $(this).data('url');
        let groupSlug = $(this).data('group-slug');
        let csrfToken = $(this).data('csrf-token');
        
            $.ajax(
            {
                url: url,
                method: 'POST',
                data: { user_id: userId, group_slug: groupSlug, csrfmiddlewaretoken: csrfToken },
                success: function (data) {
                    $("#ajax-response").html(data.response);
                    $("#ajax-response").show();
                    $(".ajax-content").load(" .ajax-load-content");
                    
                }
            }
            )
        });
    $(document).on('click', '.btn-ajax-like', function () {
        let modelId = $(this).data('model-id');
        let modelType = $(this).data('model-type');
        let url = $(this).data('url');
        let csrfToken = $(this).data('csrf-token');
        
            $.ajax(
            {
                url: url,
                method: 'POST',
                data: { model_id: modelId, model_type: modelType, csrfmiddlewaretoken: csrfToken },
                success: function (data) {
                    $("#ajax-response").html(data.response);
                    $("#ajax-response").show();
                    $("#like-btn").css('background', 'red')
                    // $(".ajax-content").load(" .ajax-load-content");
                    
                }
            }
            )
        });


        var searchRequest2 = null;
        var minlength2 = 2;
        var mashinAPI2 = "/api/search/";
        $(document).on('input', ".full-search.gui-input", function () {
          clearTimeout(this.delay);
          this.delay = setTimeout(function () {
    
            var id, title, type, q, that = this, value = $(this).val();
            let dataField =$(this).data('field');
            let dataModel =$(this).data('model');
            if (value.length >= 2) {
              $(this).addClass("border-searchresult");
              $(this).addClass("ldr");
            }
            if (value.length < 2){
                $(this).removeClass("ldr");
            }
            var resultclass = 'json-result2'
            if (value.length >= minlength2) {
                console.log(mashinAPI2);
                
              $.getJSON(mashinAPI2, {
                model:dataModel,
                field:dataField,
                value: value,

              }).done(function (data) {
                if (data.length) {
                  var output = '<ul class="searchresult" style="left:-20px;">';
                  $.each(data, function (i, item) {
                    output += '<li data-title="' + item.username + '" data-id="' + item.id + '">';
                    output += '<span>' + item.username + '</span>';
                    output += '</li>';
    
                    if (i === 5) {
                      return false;
                    }
                  });
                  output += '</ul>';
                  $(that).siblings('.' + resultclass).show().html(output);
                } else {
                  var output = '<ul class="searchresult" style="left:-20px;">';
                  output += '<li>';
                  output += '<span>هیچ موردی یافت نشد</span>';
                  output += '</li>';
                  output += '</ul>';
                  $(that).siblings('.' + resultclass).show().html(output);
                }
              }).fail(function () {
                console.log("error");
              }).always(function () {
    
              });
            } else {
              $(that).siblings('.' + resultclass).hide();
            }
          }.bind(this), 800);
        });

    // $(document).on('click', '.form-search', function () {
    //     let searched = $(this).data('search');
    //     let url = $(this).data('url');
    //     // let csrfToken = $(this).data('csrf-token');
        
    //         $.ajax(
    //         {
    //             url: url,
    //             method: 'GET',
    //             data: { search: searched },
    //             success: function () {
    //                 $(".ajax-content").load(" .ajax-load-content");
                    
    //             }
    //         }
    //         )
    //     });
});