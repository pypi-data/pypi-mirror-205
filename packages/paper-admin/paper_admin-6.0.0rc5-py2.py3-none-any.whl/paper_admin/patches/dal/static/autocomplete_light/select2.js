/*!
 * Django Autocomplete Light - Select2 function
 *
 * FIX: commented `containerCssClass`
 */

document.addEventListener("dal-init-function", function () {
    yl.registerFunction("select2", function ($, element) {
        var $element = $(element);

        // Templating helper
        function template(text, is_html) {
            if (is_html) {
                var $result = $("<span>");
                $result.html(text);
                return $result;
            } else {
                return text;
            }
        }

        function result_template(item) {
            var text = template(
                item.text,
                ($element.attr("data-html") !== undefined || $element.attr("data-result-html") !== undefined) &&
                    !item.create_id
            );

            if (item.create_id) {
                return $("<span>").text(text).addClass("dal-create");
            } else {
                return text;
            }
        }

        function selected_template(item) {
            if (item.selected_text !== undefined) {
                return template(
                    item.selected_text,
                    $element.attr("data-html") !== undefined || $element.attr("data-selected-html") !== undefined
                );
            } else {
                return result_template(item);
            }
            return;
        }

        var ajax = null;
        if ($element.attr("data-autocomplete-light-url")) {
            ajax = {
                url: $element.attr("data-autocomplete-light-url"),
                dataType: "json",
                delay: 250,

                data: function (params) {
                    var data = {
                        q: params.term, // search term
                        page: params.page,
                        create: $element.attr("data-autocomplete-light-create") && !$element.attr("data-tags"),
                        forward: yl.getForwards($element)
                    };

                    return data;
                },
                processResults: function (data, page) {
                    if ($element.attr("data-tags")) {
                        $.each(data.results, function (index, value) {
                            value.id = value.text;
                        });
                    }

                    return data;
                },
                cache: true
            };
        }

        $element.select2({
            width: "",
            tokenSeparators: $element.attr("data-tags") ? [","] : null,
            debug: true,
            // containerCssClass: ':all:',
            placeholder: $element.attr("data-placeholder") || "",
            language: $element.attr("data-autocomplete-light-language"),
            minimumInputLength: $element.attr("data-minimum-input-length") || 0,
            allowClear: !$element.is("[required]"),
            templateResult: result_template,
            templateSelection: selected_template,
            ajax: ajax,
            with: null,
            tags: Boolean($element.attr("data-tags"))
        });

        $element.on("select2:selecting", function (e) {
            var data = e.params.args.data;

            if (data.create_id !== true) return;

            e.preventDefault();

            var select = $element;

            $.ajax({
                url: $element.attr("data-autocomplete-light-url"),
                type: "POST",
                dataType: "json",
                data: {
                    text: data.id,
                    forward: yl.getForwards($element)
                },
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", document.csrftoken);
                },
                success: function (data, textStatus, jqXHR) {
                    select.append($("<option>", { value: data.id, text: data.text, selected: true }));
                    select.trigger("change");
                    select.select2("close");
                }
            });
        });
    });
});
