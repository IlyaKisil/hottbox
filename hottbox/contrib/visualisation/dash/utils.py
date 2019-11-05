class DynamicComponentsID(object):

    def __init__(self, elements):
        self.ids = dict()
        for prefix, number in elements.items():
            self.ids[prefix] = [f"{prefix}-{i}" for i in range(number)]

    def get_by_number(self, prefix, number=None):
        if number is None:
            return self.ids[prefix][0]
        else:
            return self.ids[prefix][number]

    def get_by_id(self, prefix, id):
        return self.ids[prefix].index(id)


def generate_dropdown_options(options_list):
    return [{'label': i, 'value': i} for i in options_list]
