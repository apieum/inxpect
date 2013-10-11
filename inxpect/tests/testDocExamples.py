# -*- coding: utf8 -*-
from . import TestCase
import inxpect

class Subject(object):
    args = tuple()
    kwargs = dict()
    def __call__(self, event):
        self.args = event.args
        self.kwargs = event.kwargs
        event.result = False

class EventData(object):
    name = 'event'
    subject = Subject()
    args = tuple()
    kwargs = dict()
    result = True

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)

class DocExamplesTest(TestCase):
    def test_Inspect(self):

        expect = inxpect.expect_factory(EventData)
        assert hasattr(expect, 'result')
        assert hasattr(expect.subject, 'args') == False
        # with depth to 1:
        expect = inxpect.expect_factory(EventData, 1)
        assert hasattr(expect.subject, 'args')

    def test_Expect_basics(self):

        expect = inxpect.expect_factory(EventData)

        name_is_event1 = expect.name.equal_to('event1')  # can be done with ==
        result_is_not_None = expect.result != None
        is_event1 = name_is_event1 & result_is_not_None

        event1 = EventData(name='event1')
        event2 = EventData(name='event2', result=None)

        assert result_is_not_None(event1)
        assert result_is_not_None(event2) == False

        assert name_is_event1(event1)
        assert name_is_event1(event2) == False

        log = []
        expected = 'Name %s is not "event1"'

        def is_event1_fails(chain, at, *args, **kwargs):
            # args and kwargs are same passed to is_event1:
            event = args[0]
            if at in name_is_event1:
                log.append(expected % event.name)
            return False

        is_event1.on_fail(is_event1_fails)

        assert is_event1(event1)
        assert is_event1(event2) == False

        assert log[0] == expected % 'event2'
