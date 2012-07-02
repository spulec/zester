from collections import namedtuple
import inspect
import os

from ghost import Ghost


class Client(object):
    def __init__(self):
        assert self.url
        self._attributes = self._collect_attributes()
        self._class_model = self._setup_class_model()
        self._ghost = Ghost()

    def process(self):
        self._load_ghost()
        self._results = self._process_attributes()
        return self._results

    def _setup_class_model(self):
        class_name = self.__class__.__name__
        return namedtuple(class_name + "Response", self._attributes.keys())

    def _collect_attributes(self):
        attrs = [(attr_name, attr) for (attr_name, attr) in
            inspect.getmembers(self) if isinstance(attr, Attribute)]
        return dict(attrs)

    def _process_attributes(self):
        results = []
        for attribute_name, attribute in self._attributes.iteritems():
            result, resources = self._ghost.evaluate(attribute.query)
            if result:
                results.append(result)
        if not results:
            return results
        zipped_results = zip(*results)
        final_results = []
        attribute_names = self._attributes.keys()
        for zipped_result in zipped_results:
            result_dict = dict(zip(attribute_names, zipped_result))
            final_results.append(self._class_model(**result_dict))
        return final_results

    def _load_ghost(self):
        page, extra_resources = self._ghost.open(self.url)

        # For local testing, page is None
        if page:
            # TODO should error better
            assert page.http_status < 400

        # Load jquery
        jquery_path = os.path.join(os.path.abspath(os.curdir),
                            'zester', 'fixtures', 'jquery.min.js')
        jquery_text = open(jquery_path, 'r').read()
        result, resources = self._ghost.evaluate(jquery_text)


class Attribute(object):

    def __init__(self, selector, modifier):
        self.selector = selector
        self.modifier = modifier

    @property
    def query(self):
        if self.modifier:
            # Escaping braces in here
            base = "$.map({selector}, function(el){{ return {modifier}}});"
            return base.format(selector=self.selector, modifier=self.modifier)
        else:
            return "$({selector})".format(selector=self.selector)
