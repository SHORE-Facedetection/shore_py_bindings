"""Module providing an easy-to-use wrapper around the Shore API

Copyright (c) 2019 Fraunhofer IIS and shore_py_bindings contributors.

This file is part of shore_py_bindings which is released under MIT license.
See file LICENSE for full license details.
"""
import collections.abc

import shore


__version__ = shore.Version()

_COLOR_SPACES = ('GRAYSCALE', 'RGB', 'BGR')


def create_face_engine(*args, **kwargs):
    """Create a Shore engine for face processing

    Refer to the main Shore documentation for function parameters.

    Returns the ShoreEngine instance.
    """
    return ShoreEngine(shore.CreateFaceEngine(*args, **kwargs))


def create_engine(setupScript, setupCall):
    """Create a Shore engine with a Lua script

    Refer to the main Shore documentation for function parameters.

    Returns the ShoreEngine instance.
    """
    return ShoreEngine(shore.CreateEngine(setupScript, setupCall))


class ShoreEngine:
    """Shore engine

    Refer to the main Shore documentation for parameters.
    """
    def __init__(self, engine):
        if not isinstance(engine, shore.Engine):
           raise TypeError('Expected type ShoreEngine, got `{}`'
                           .format(type(engine)))
        self._engine = engine

    def __call__(self, image, color_space='GRAYSCALE'):
        """Use Shore to process an image

        Returns a content object.
        """
        if color_space not in _COLOR_SPACES:
            raise ValueError('Unsupported color space `{}`'
                             .format(color_space))
        return ShoreContent(self._engine.Process(image, color_space))

    def __del__(self):
        if hasattr(self, '_engine') and self._engine:
            shore.DeleteEngine(self._engine)


class ShoreContent:
    def __init__(self, content):
        self._content = content
        self._num_objects = content.getObjectCount()
        self._num_infos = content.getInfoCount()

    @property
    def num_objects(self):
        """Number of objects of this content"""
        return self._num_objects

    @property
    def num_infos(self):
        """Number of infos of this content"""
        return self._num_infos

    def objects(self):
        """Iterator over objects of this content"""
        for idx in range(self._num_objects):
            yield ShoreObject(self._content.getObject(idx))

    def infos(self):
        """Dictionary over infos of this content"""
        return _DictWrapper(self._num_infos,
                            self._content.getInfoKey,
                            self._content.getInfo,
                            self._content.getInfoOf)

    def __str__(self):
        return ('ShoreContent with {} object(s) and {} info(s)'
                .format(self._num_objects, self._num_infos))


class ShoreObject:
    def __init__(self, obj):
        self._obj = obj
        self._num_markers = obj.getMarkerCount()
        self._num_attributes = obj.getAttributeCount()
        self._num_ratings = obj.getRatingCount()
        self._num_parts = obj.getPartCount()

    @property
    def type(self):
        """Type of this object"""
        return self._obj.getType()

    @property
    def region(self):
        """Region of this object"""
        return ShoreRegion(self._obj.getRegion())

    def markers(self):
        """Dictionary over markers of this objects"""
        return _DictWrapper(self._num_markers,
                            self._obj.getMarkerKey,
                            self._obj.getMarker,
                            self._obj.getMarkerOf,
                            ShoreMarker)

    def attributes(self):
        """Dictionary over attributes of this objects"""
        return _DictWrapper(self._num_attributes,
                            self._obj.getAttributeKey,
                            self._obj.getAttribute,
                            self._obj.getAttributeOf)

    def ratings(self):
        """Dictionary over ratings of this objects"""
        return _DictWrapper(self._num_ratings,
                            self._obj.getRatingKey,
                            self._obj.getRating,
                            self._obj.getRatingOf)

    def parts(self):
        """Dictionary over parts of this objects"""
        return _DictWrapper(self._num_parts,
                            self._obj.getPartKey,
                            self._obj.getPart,
                            self._obj.getPartOf,
                            ShoreObject)

    def __str__(self):
        return 'ShoreObject of type "{}"'.format(self.type)

    def __repr__(self):
        s = 'ShoreObject of type "{}"\n'.format(self.type)
        s += '- Region: {}\n'.format(self.region)
        if self._num_markers > 0:
            s += '- Markers:\n'
            for key, marker in self.markers().items():
                s += '  * {}: {}\n'.format(key, marker)
        else:
            s += '- Markers: None\n'
        if self._num_attributes > 0:
            s += '- Attributes:\n'
            for key, attribute in self.attributes().items():
                s += '  * {}: {}\n'.format(key, attribute)
        else:
            s += '- Attributes: None\n'
        if self._num_ratings > 0:
            s += '- Ratings:\n'
            for key, rating in self.ratings().items():
                s += '  * {}: {}\n'.format(key, rating)
        else:
            s += '- Ratings: None\n'
        if self._num_parts > 0:
            s += '- Parts:\n'
            for key, part in self.parts().items():
                s += '  * {}: {}\n'.format(key, part)
        else:
            s += '- Parts: None\n'

        if s[-1:] == '\n':
            return s[:-1]
        else:
            return s


class ShoreRegion:
    def __init__(self, region):
        self._left = region.getLeft()
        self._top = region.getTop()
        self._right = region.getRight()
        self._bottom = region.getBottom()

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top

    @property
    def right(self):
        return self._right

    @property
    def bottom(self):
        return self._bottom

    def __iter__(self):
        yield self._left
        yield self._top
        yield self._right
        yield self._bottom

    def __str__(self):
        return '(({}, {}), ({}, {}))'.format(self._left, self._top,
                                             self._right, self._bottom)

    def __repr__(self):
        return 'ShoreRegion {}'.format(self)


class ShoreMarker:
    def __init__(self, marker):
        self._x = marker.getX()
        self._y = marker.getY()

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __iter__(self):
        yield self._x
        yield self._y

    def __str__(self):
        return '({}, {})'.format(self._x, self._y)

    def __repr__(self):
        return 'ShoreMarker {}'.format(self)


class _DictWrapper(collections.abc.Mapping):
    def __init__(self,
                 num_items,
                 key_accessor,
                 item_accessor,
                 item_of_accessor,
                 item_constructor=None):
        self._num_items = num_items
        self._key_accessor = key_accessor
        self._item_accessor = item_accessor
        self._item_of_accessor = item_of_accessor
        self._item_constructor = item_constructor

    def __getitem__(self, key):
        if self._item_constructor is None:
            return self._item_of_accessor(key)
        else:
            return self._item_constructor(self._item_of_accessor(key))

    def __iter__(self):
        return (self._key_accessor(idx) for idx in range(self._num_items))

    def values(self):
        if self._item_constructor is None:
            return (self._item_accessor(idx) for idx in range(self._num_items))
        else:
            return (self._item_constructor(self._item_accessor(idx))
                    for idx in range(self._num_items))

    def items(self):
        if self._item_constructor is None:
            return ((self._key_accessor(idx), self._item_accessor(idx))
                    for idx in range(self._num_items))
        else:
            return ((self._key_accessor(idx),
                     self._item_constructor(self._item_accessor(idx)))
                    for idx in range(self._num_items))

    def __len__(self):
        return self._num_items
