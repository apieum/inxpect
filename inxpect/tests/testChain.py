# -*- coding: utf8 -*-
from . import TestCase, Mock
from inxpect.expect.chain import AndChain, OrChain


class AndChainTest(TestCase):
    def test_it_should_call_each_callback_it_contains_until_false(self):
        callback1 = Mock(return_value=True)
        callback2 = Mock(return_value=False)
        callback3 = Mock(return_value=True)
        conditions = AndChain(callback1, callback2, callback3)
        args = ('arg1', 'arg2')
        self.assertFalse(conditions(*args))
        callback1.assert_called_once_with(*args)
        callback2.assert_called_once_with(*args)
        self.assertEqual(callback3.call_count, 0)

    def test_can_chain_conditions_with_bitwise_or(self):
        callback1 = Mock(return_value=True)
        callback2 = Mock(return_value=False)
        cond1 = AndChain(callback1) | AndChain(callback2)
        cond2 = AndChain(callback2) | AndChain(callback1)
        self.assertTrue(cond1())
        self.assertTrue(cond2())

    def test_can_chain_conditions_with_bitwise_and(self):
        callback1 = Mock(return_value=True)
        callback2 = Mock(return_value=False)
        cond1 = AndChain(callback1) & AndChain(callback2)
        cond2 = AndChain(callback2) & AndChain(callback1)
        self.assertFalse(cond1())
        self.assertFalse(cond2())

    def test_can_raises_an_exception_when_fail(self):
        expected = 'it fails'
        def fail(chain, at, *args, **kwargs):
            raise AssertionError('it fails')
        cond = AndChain(Mock(return_value=False))
        cond.on_fail(fail)
        with self.assertRaisesRegex(AssertionError, expected):
            cond()

    def test_can_log_result_when_succeed(self):
        message = "ok with: %s and %s"
        logs = []
        def log(chain, *args, **kwargs):
            logs.append(message %(args, kwargs))
        cond = AndChain(Mock(return_value=True))
        cond.on_success(log)
        expected_logs = [
            message %(tuple(), {}),
            message %(('arg1', 'arg2'), {'kwarg1':'val1'})
        ]
        cond()
        cond('arg1', 'arg2', kwarg1='val1')
        self.assertEqual(logs, expected_logs)

    def test_it_returns_OrCondition_when_chaining_with_bitwise_or(self):
        callback1 = Mock(return_value=True)
        callback2 = Mock(return_value=False)
        condition = AndChain(callback1) | AndChain(callback2)
        self.assertIsInstance(condition, OrChain)

    def test_it_just_extend_when_chaining_with_bitwise_and(self):
        callback1 = Mock(return_value=True)
        callback2 = Mock(return_value=False)
        condition1 = AndChain(callback1)
        condition2 = condition1 & AndChain(callback2)
        self.assertIs(condition1, condition2)
        self.assertIn(callback2, condition2)



class OrChainTest(TestCase):
    def test_it_returns_true_at_first_callback_that_returns_true(self):
        callback1 = Mock(return_value=False)
        callback2 = Mock(return_value=True)
        callback3 = Mock(return_value=True)
        conditions = OrChain(callback1, callback2, callback3)
        args = ('arg1', 'arg2')
        self.assertTrue(conditions(*args))
        callback1.assert_called_once_with(*args)
        callback2.assert_called_once_with(*args)
        self.assertEqual(callback3.call_count, 0)

    def test_it_returns_AndCondition_when_chaining_with_bitwise_and(self):
        callback1 = Mock(return_value=True)
        callback2 = Mock(return_value=False)
        condition = OrChain(callback1) & OrChain(callback2)
        self.assertIsInstance(condition, AndChain)

    def test_it_just_extend_when_chaining_with_bitwise_or(self):
        callback1 = Mock(return_value=False)
        callback2 = Mock(return_value=True)
        condition1 = OrChain(callback1)
        condition2 = condition1 | OrChain(callback2)
        self.assertIs(condition1, condition2)
        self.assertIn(callback2, condition2)

    def test_it_is_searchable(self):
        from inxpect.expect.operator import Equal
        from inxpect.expect.getters import AsIs
        list1 = [OrChain(Equal(True, AsIs(True)))]
        self.assertIn(OrChain(Equal(True, AsIs(True))), list1)



