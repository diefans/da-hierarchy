# -*- coding: utf-8 -*-
# pylint: disable-all

import unittest
import fudge

from da.utils import hierarchy


class TestHierarchyNode(unittest.TestCase):

    def test_init(self):
        n = hierarchy.HierarchyNode(dict(a='b'), b='c')

        self.assertTrue(hasattr(n, '_parent'))
        self.assertEqual(n, {'a': 'b', 'b': 'c', 'children': []})

    def test_keys_as_attributes(self):
        n = hierarchy.HierarchyNode(a='b')


        self.assertTrue(hasattr(n, 'a'))
        self.assertEqual(n.a, 'b')

        self.assertRaises(AttributeError, getattr, n, 'b')

    def test_rename_children(self):
        n = hierarchy.HierarchyNode()
        n.rename_children('kinder')

        self.assertEqual(n, {'kinder': []})

    def test_set_parent(self):
        n1 = hierarchy.HierarchyNode(id=1)
        n2 = hierarchy.HierarchyNode(id=2)
        n3 = hierarchy.HierarchyNode(id=3)
        n1.parent = n2

        self.assertEqual(n2, {'id': 2, 'children': [{'id': 1, 'children': []}]})
        self.assertEqual(n1._parent, n2)
        self.assertEqual(n1._parent, n1.parent)

        # moving to other parent
        n1.parent = n3
        self.assertEqual(n2, {'id': 2, 'children': []})
        self.assertEqual(n3, {'id': 3, 'children': [{'id': 1, 'children': []}]})
        self.assertEqual(n1._parent, n3)

    def test_misuse_parent(self):
        n1 = hierarchy.HierarchyNode(id=1)
        n2 = hierarchy.HierarchyNode(id=2)
        n3 = hierarchy.HierarchyNode(id=3)

        n1._parent = n2

        self.assertRaises(ValueError, setattr, n1, 'parent', n3)

    def test_parents(self):
        n1 = hierarchy.HierarchyNode(id=1)
        n2 = hierarchy.HierarchyNode(id=2)
        n3 = hierarchy.HierarchyNode(id=3)

        n1.parent = n2
        n2.parent = n3

        self.assertEqual(n1.parents, [n2, n3])

    def test_depth(self):
        n1 = hierarchy.HierarchyNode(id=1)
        n2 = hierarchy.HierarchyNode(id=2)
        n3 = hierarchy.HierarchyNode(id=3)

        n1.parent = n2
        n2.parent = n3

        self.assertEqual(n1.depth, 2)

    def test_add(self):
        p = hierarchy.HierarchyNode()
        c = p.add(foo='bar')

        self.assertNotEqual(p, c)
        self.assertTrue(c in p.children)
        self.assertEqual(p.children[0].foo, 'bar')

class TestObject(object):
    def __init__(self, **kw):
        for k, v in kw.iteritems():
            setattr(self, k, v)

class TestHierarchyList(unittest.TestCase):
    def setUp(self):
        # create a list of related objects
        self.iterable = [TestObject(id=1, parent_id=None, data=1),
                         TestObject(id=2, parent_id=None, data=2),
                         TestObject(id=3, parent_id=None, data=3),
                         TestObject(id=4, parent_id=1, data=4),
                         TestObject(id=5, parent_id=2, data=5),
                         TestObject(id=6, parent_id=3, data=6),
                         TestObject(id=7, parent_id=4, data=7),
                         TestObject(id=8, parent_id=5, data=8),
                         TestObject(id=9, parent_id=6, data=9),
                         TestObject(id=10, parent_id=7, data=10),
                         ]
    def test_init(self):
        h = hierarchy.HierarchyList(self.iterable)

        self.assertEqual(h, [{'children': [{'children': [{'children': [{'children': []}]}]}]},
                             {'children': [{'children': [{'children': []}]}]},
                             {'children': [{'children': [{'children': []}]}]}])

    def test_init_with_callback(self):
        def cb(item, node, hlist):
            node['d'] = item.data
        h = hierarchy.HierarchyList(self.iterable, callback=cb)

        self.assertEqual(h, [{'children': [{'children': [{'children': [{'children': [], 'd': 10}], 'd': 7}], 'd': 4}], 'd': 1},
                             {'children': [{'children': [{'children': [], 'd': 8}], 'd': 5}], 'd': 2},
                             {'children': [{'children': [{'children': [], 'd': 9}], 'd': 6}], 'd': 3}])

    def test_iterindex(self):
        def cb(item, node, hlist):
            node['d'] = item.data
        h = hierarchy.HierarchyList(self.iterable, callback=cb)

        self.assertEqual(h.iterindex(), [{'children': [{'children': [{'children': [{'children': [], 'd': 10}], 'd': 7}], 'd': 4}], 'd': 1},
                                         {'children': [{'children': [{'children': [], 'd': 8}], 'd': 5}], 'd': 2},
                                         {'children': [{'children': [{'children': [], 'd': 9}], 'd': 6}], 'd': 3},
                                         {'children': [{'children': [{'children': [], 'd': 10}], 'd': 7}], 'd': 4},
                                         {'children': [{'children': [], 'd': 8}], 'd': 5},
                                         {'children': [{'children': [], 'd': 9}], 'd': 6},
                                         {'children': [{'children': [], 'd': 10}], 'd': 7},
                                         {'children': [], 'd': 8},
                                         {'children': [], 'd': 9},
                                         {'children': [], 'd': 10}])

    def test_idx(self):
        def cb(item, node, hlist):
            node['d'] = item.data
        h = hierarchy.HierarchyList(self.iterable, callback=cb)

        self.assertEqual(h.idx, {1: {'children': [{'children': [{'children': [{'children': [], 'd': 10}], 'd': 7}], 'd': 4}], 'd': 1},
                                 2: {'children': [{'children': [{'children': [], 'd': 8}], 'd': 5}], 'd': 2},
                                 3: {'children': [{'children': [{'children': [], 'd': 9}], 'd': 6}], 'd': 3},
                                 4: {'children': [{'children': [{'children': [], 'd': 10}], 'd': 7}], 'd': 4},
                                 5: {'children': [{'children': [], 'd': 8}], 'd': 5},
                                 6: {'children': [{'children': [], 'd': 9}], 'd': 6},
                                 7: {'children': [{'children': [], 'd': 10}], 'd': 7},
                                 8: {'children': [], 'd': 8},
                                 9: {'children': [], 'd': 9},
                                 10: {'children': [], 'd': 10}})

    def test_iterleaves(self):
        def cb(item, node, hlist):
            node['d'] = item.data
        h = hierarchy.HierarchyList(self.iterable, callback=cb)

        self.assertEqual(list(h.iterleaves()), [{'children': [], 'd': 8},
                                         {'children': [], 'd': 9},
                                         {'children': [], 'd': 10}])

    def test_iternodes(self):
        def cb(item, node, hlist):
            node['d'] = item.data
        h = hierarchy.HierarchyList(self.iterable, callback=cb)

        self.assertEqual(list(h.iternodes()), [{'children': [{'children': [{'children': [{'children': [], 'd': 10}], 'd': 7}], 'd': 4}], 'd': 1},
                                         {'children': [{'children': [{'children': [], 'd': 8}], 'd': 5}], 'd': 2},
                                         {'children': [{'children': [{'children': [], 'd': 9}], 'd': 6}], 'd': 3},
                                         {'children': [{'children': [{'children': [], 'd': 10}], 'd': 7}], 'd': 4},
                                         {'children': [{'children': [], 'd': 8}], 'd': 5},
                                         {'children': [{'children': [], 'd': 9}], 'd': 6},
                                         {'children': [{'children': [], 'd': 10}], 'd': 7}])
