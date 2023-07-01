from django.forms.widgets import Widget
from django.utils.safestring import mark_safe


class DualSliderWidget(Widget):
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ['', '']  # Set default values if no value is provided
        else:
            value = [str(v) for v in value]  # Convert the values to strings

        final_attrs = self.build_attrs(attrs, type='text', name=name)

        # Generate the HTML markup for the dual slider widget
        slider_html = '''
            <div id="{id}_slider"></div>
            <input type="hidden" id="{id}_min" name="{name}_min" value="{value_min}">
            <input type="hidden" id="{id}_max" name="{name}_max" value="{value_max}">
        '''.format(id=final_attrs['id'], name=name, value_min=value[0], value_max=value[1])

        script_html = '''
            <script type="text/javascript">
                $(function() {{
                    $("#{id}_slider").slider({{
                        range: true,
                        min: {min},
                        max: {max},
                        values: [{value_min}, {value_max}],
                        slide: function(event, ui) {{
                            $("#{id}_min").val(ui.values[0]);
                            $("#{id}_max").val(ui.values[1]);
                        }}
                    }});
                }});
            </script>
        '''.format(id=final_attrs['id'], min=0, max=100, value_min=value[0], value_max=value[1])

        # Combine the HTML markup for the slider and the JavaScript code
        output = slider_html + script_html
        return mark_safe(output)