"""frosted/reporter.py.

Defines the error messages that frosted can output

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR

"""

from __future__ import absolute_import, division, print_function, unicode_literals

from collections import namedtuple

from pies.overrides import *

BY_CODE = {}

AbstractMessageType = namedtuple('AbstractMessageType', ('error_code', 'name', 'template'))


class MessageType(AbstractMessageType):

    class Message(namedtuple('Message', ('message', 'type', 'lineno', 'col'))):

        def __str__(self):
            return self.message

    def __new__(cls, error_code, name, template):
        new_instance = AbstractMessageType.__new__(cls, error_code, name, template)
        BY_CODE[error_code] = new_instance
        return new_instance

    def __call__(self, filename, loc=None, *kargs, **kwargs):
        values = {'filename': filename, 'lineno':loc.lineno, 'col': getattr(loc, 'col_offset', 0)}
        values.update(kwargs)
        return self.Message('{0}:{1}: {2}'.format(filename, values['lineno'], self.template.format(*kargs, **values)),
                            self, values['lineno'], values['col'])


class OffsetMessageType(MessageType):
    def __call__(self, filename, loc, position=None, *kargs, **kwargs):
        if position:
            kwargs.update({'lineno': position[0], 'col': position[1]})
        return MessageType.__call__(self, filename, loc, *kargs, **kwargs)


Message = MessageType(100, 'Generic', '{0}')
UnusedImport = MessageType(101, 'UnusedImport', '{0} imported but unused')
RedefinedWhileUnused = MessageType(102, 'RedefinedWhileUnused',
                                   'redefinition of {0!r} from line {1.lineno!r}')
RedefinedInListComp = MessageType(103, 'RedefinedInListComp',
                                  'list comprehension redefines {0!r} from line {1.lineno!r}')
ImportShadowedByLoopVar = MessageType(104, 'ImportShadowedByLoopVar',
                                      'import {0!r} from line {1.lineno!r} shadowed by loop variable')
ImportStarUsed = MessageType(105, 'ImportStarUsed', "'from {0!s} import *' used; unable to detect undefined names")
UndefinedName = MessageType(106, 'UndefinedName', "undefined name {0!r}")
DoctestSyntaxError = OffsetMessageType(107, 'DoctestSyntaxError', "syntax error in doctest")
UndefinedExport = MessageType(108, 'UndefinedExport', "undefined name {0!r} in __all__")
UndefinedLocal = MessageType(109, 'UndefinedLocal',
                  'local variable {0!r} (defined in enclosing scope on line {1.lineno!r}) referenced before assignment')
DuplicateArgument = MessageType(110, 'DuplicateArgument', "duplicate argument {0!r} in function definition")
Redefined = MessageType(111, 'Redefined', "redefinition of {0!r} from line {1.lineno!r}")
LateFutureImport = MessageType(112, 'LateFutureImport', "future import(s) {0!r} after other statements")
UnusedVariable = MessageType(113, 'UnusedVariable', "local variable {0!r} is assigned to but never used")
MultipleValuesForArgument = MessageType(114, 'MultipleValuesForArgument',
                                        "{0!s}() got multiple values for argument {1!r}")
TooFewArguments = MessageType(115, 'TooFewArguments', "{0!s}() takes at least {1:d} argument(s)")
TooManyArguments = MessageType(116, 'TooManyArguments', "{0!s}() takes at most {1:d} argument(s)")
UnexpectedArgument = MessageType(117, 'UnexpectedArgument', "{0!s}() got unexpected keyword argument: {1!r}")
NeedKwOnlyArgument = MessageType(118, 'NeedKwOnlyArgument', "{0!s}() needs kw-only argument(s): {1!s}")
ReturnWithArgsInsideGenerator = MessageType(119, 'ReturnWithArgsInsideGenerator',
                                            "'return' with argument inside generator")
