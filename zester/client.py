from collections import namedtuple
import inspect
import os

from ghost import Ghost


class Client(object):
    def __init__(self, url=None):
        if url:
            self.url = url
        assert self.url, "All clients must have a URL attribute"
        self._attributes = self._collect_attributes()
        self._class_model = self._setup_class_model()
        self._ghost = Ghost()

    def process(self):
        self._load_ghost()
        attribute_results = self._process_attributes()
        self._object_results = self._make_objects(attribute_results)
        return self._object_results

    def _setup_class_model(self):
        class_name = self.__class__.__name__
        return namedtuple(class_name + "Response", self._attributes.keys())

    def _process_attributes(self):
        results = []
        for attribute_name, attribute in self._attributes.iteritems():
            result, resources = self._ghost.evaluate(attribute.query)
            # If a node was selected, return it's data
            if isinstance(result, dict):
                if 'data' in result:
                    result = result['data']
                elif 'selector' in result:
                    raise TypeError("The attribute {} returned a selector"
                        " instead of a node.".format(attribute_name))
            results.append(result)
        return results

    def _make_objects(self, attribute_results):
        raise NotImplementedError()

    def _collect_attributes(self):
        attrs = [(attr_name, attr) for (attr_name, attr) in
            inspect.getmembers(self) if isinstance(attr, Attribute)]
        return dict(attrs)

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


class MultipleClient(Client):
    def _process_attributes(self):
        results = super(MultipleClient, self)._process_attributes()
        if not results:
            return results
        zipped_results = zip(*results)
        return zipped_results

    def _make_objects(self, attribute_results):
        object_results = []
        attribute_names = self._attributes.keys()
        for attribute_result in attribute_results:
            result_dict = dict(zip(attribute_names, attribute_result))
            object_results.append(self._class_model(**result_dict))
        return object_results


class SingleClient(Client):
    def _process_attributes(self):
        result = super(SingleClient, self)._process_attributes()
        number_of_attributes = len(self._attributes)
        if len(result) > number_of_attributes:
            # If we found more attributes than we were looking for
            result = result[:number_of_attributes]
        return result

    def _make_objects(self, attribute_result):
        attribute_names = self._attributes.keys()
        result_dict = dict(zip(attribute_names, attribute_result))
        object_result = self._class_model(**result_dict)
        return object_result


class Attribute(object):

    def __init__(self, selector, modifier=None):
        self.selector = selector
        self.modifier = modifier

    @property
    def query(self):
        if self.modifier:
            # Escaping braces in here
            base = "$.map({selector}, function(el){{ return {modifier}}});"
            return base.format(selector=self.selector, modifier=self.modifier)
        else:
            return self.selector
