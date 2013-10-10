# -*- coding: utf8 -*-
from . import TestCase, Mock
from inxpect.expect.chain import Chain


class ChainTest(TestCase):
    def test_it_should_call_each_callback_it_contains_until_false(self):
        callback1 = Mock(return_value=True)
        callback2 = Mock(return_value=False)
        callback3 = Mock(return_value=True)
        conditions = Chain(callback1, callback2, callback3)
        args = ('arg1', 'arg2')
        self.assertFalse(conditions(*args))
        callback1.assert_called_once_with(*args)
        callback2.assert_called_once_with(*args)
        self.assertEqual(callback3.call_count, 0)

    def test_can_chain_conditions_with_bitwise_or(self):
        callback1 = Mock(return_value=True)
        callback2 = Mock(return_value=False)
        cond1 = Chain(callback1) | Chain(callback2)
        cond2 = Chain(callback2) | Chain(callback1)
        self.assertTrue(cond1())
        self.assertTrue(cond2())

    def test_can_chain_conditions_with_bitwise_and(self):
        callback1 = Mock(return_value=True)
        callback2 = Mock(return_value=False)
        cond1 = Chain(callback1) & Chain(callback2)
        cond2 = Chain(callback2) & Chain(callback1)
        self.assertFalse(cond1())
        self.assertFalse(cond2())

    def test_can_raises_an_exception_when_fail(self):
        expected = 'it fails'
        def fail(chain, at, *args, **kwargs):
            raise AssertionError('it fails')
        cond = Chain(Mock(return_value=False))
        cond.on_fail(fail)
        with self.assertRaisesRegex(AssertionError, expected):
            cond()

    def test_can_log_result_when_succeed(self):
        message = "ok with: %s and %s"
        logs = []
        def log(chain, *args, **kwargs):
            logs.append(message %(args, kwargs))
        cond = Chain(Mock(return_value=True))
        cond.on_success(log)
        expected_logs = [
            message %(tuple(), {}),
            message %(('arg1', 'arg2'), {'kwarg1':'val1'})
        ]
        cond()
        cond('arg1', 'arg2', kwarg1='val1')
        self.assertEqual(logs, expected_logs)
