def generate_plot_id(mode_name):
    return f"graph-{mode_name}"


def generate_title_input_id(mode_name):
    return f"input-title-{mode_name}"


def generate_component_dropdown_id(mode_name):
    return f"dropdown-component-{mode_name}"


def generate_dash_element_id():
    pass


def generate_dropdown_options(options_list):
    return [{'label': i, 'value': i} for i in options_list]
