#!../venv/bin/pytest -s

from confattr import Config, ConfigFile, Message

import sys
import pytest


class ParseError(ValueError):
	pass

def ui_callback(msg: Message) -> None:
	raise ParseError(msg)


# ------- expand_config -------

def test_expand_config() -> None:
	a = Config('a', 42, unit='')
	b = Config('b', 'foo')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="a is %a%"')
	assert b.value == 'a is 42'

def test_expand_config_format_value() -> None:
	a = Config('a', 42, unit='')
	b = Config('b', 'foo')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="%a% = 0x%a:02X%"')
	assert b.value == '42 = 0x2A'

def test_expand_config_format_default() -> None:
	a = Config('a', True)
	b = Config('b', 'foo')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="|%a!:^20%|"')
	assert b.value == '|        true        |'

def test_expand_config_format_repr() -> None:
	a = Config('a', 'hello world')
	b = Config('b', 'foo')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="and I say %a!r%"')
	assert b.value == "and I say 'hello world'"

@pytest.mark.skipif(sys.version_info < (3, 7), reason='str.isascii requires Python 3.7 or newer')
def test_expand_config_format_ascii() -> None:
	a = Config('a', 'hällo wörld')
	b = Config('b', 'foo')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="and I say %a!a%"')
	assert not a.value.isascii()
	assert 'and I say' in b.value
	assert b.value.isascii()

def test_expand_config_format_str() -> None:
	a = Config('a', True)
	b = Config('b', 'foo')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="a is %a!s%"')
	assert b.value == "a is True"

def test_expand_config_format_invalid_conversion() -> None:
	a = Config('a', True)
	b = Config('b', 'foo')
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	with pytest.raises(ParseError, match=r"invalid conversion 'foo'"):
		cf.parse_line('set b="a is %a!foo%"')
	assert b.value == "foo"

def test_expand_invalid_key() -> None:
	a = Config('a', 42, unit='')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.parse_line('set b=%foo%')

	messages: 'list[Message]' = []
	cf.set_ui_callback(messages.append)
	assert len(messages) == 1
	assert messages[0].message == "invalid key 'foo'"

def test_expand_odd_number_of_percent_characters() -> None:
	a = Config('a', 42, unit='')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.parse_line('set b=%a%%')

	messages: 'list[Message]' = []
	cf.set_ui_callback(messages.append)
	assert len(messages) == 1
	assert messages[0].message.startswith("uneven number of percent characters")   # type: ignore [union-attr]  # BaseException has no attribute "startswith"


# ------- expand_env -------

def test_expand_defined_env_normal(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', 'world')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO}"')

	assert b.value == 'hello world'

def test_expand_undefined_env_normal() -> None:
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO}"')

	assert b.value == 'hello '


def test_expand_defined_env_default_value_with_colon(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', 'universe')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:-world}"')

	assert b.value == 'hello universe'

def test_expand_undefined_env_default_value_with_colon() -> None:
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:-world}"')

	assert b.value == 'hello world'

def test_expand_empty_env_default_value_with_colon(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', '')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:-world}"')

	assert b.value == 'hello world'

def test_expand_empty_env_default_value_without_colon(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', '')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO-world}"')

	assert b.value == 'hello '


def test_expand_defined_env_assign_value_with_colon(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', 'universe')
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:=world}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert b.value == 'hello universe'
	assert c.value == 'hello universe'

def test_expand_undefined_env_assign_value_with_colon(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO' ,'')  # reset the value that I will assign during this test at the end of the test
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:=world}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert b.value == 'hello world'
	assert c.value == 'hello world'


def test_expand_defined_env_indicate_error(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', 'world')
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:?}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert b.value == 'hello world'
	assert c.value == 'hello world'

def test_expand_undefined_env_indicate_error_with_default_message() -> None:
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	messages: 'list[Message]' = []
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(messages.append)
	cf.parse_line('set b="hello ${HELLO:?}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert len(messages) == 1
	assert messages[0].message == 'environment variable HELLO is unset'

	assert b.value == 'foo'
	assert c.value == 'hello '

def test_expand_empty_env_indicate_error_with_default_message(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', '')
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	messages: 'list[Message]' = []
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(messages.append)
	cf.parse_line('set b="hello ${HELLO:?}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert len(messages) == 1
	assert messages[0].message == 'environment variable HELLO is empty'

	assert b.value == 'foo'
	assert c.value == 'hello '

def test_expand_undefined_env_indicate_error_with_custom_message() -> None:
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	messages: 'list[Message]' = []
	cf = ConfigFile(appname='test')
	cf.set_ui_callback(messages.append)
	cf.parse_line('set b="hello ${HELLO:?HELLO is required}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert len(messages) == 1
	assert messages[0].message == 'HELLO is required'

	assert b.value == 'foo'
	assert c.value == 'hello '


def test_expand_defined_env_use_alternative(monkeypatch: pytest.MonkeyPatch) -> None:
	monkeypatch.setenv('HELLO', 'universe')
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:+world}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert b.value == 'hello world'
	assert c.value == 'hello universe'

def test_expand_undefined_env_use_alternative() -> None:
	b = Config('b', 'foo')
	c = Config('c', 'bar')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b="hello ${HELLO:+world}"')
	cf.parse_line('set c="hello ${HELLO}"')

	assert b.value == 'hello '
	assert c.value == 'hello '


# ------- raw -------

def test_raw_vim_style() -> None:
	a = Config('a', 42, unit='')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set --raw b=%foo%')

	assert b.value == '%foo%'

def test_raw_vim_style_partly() -> None:
	a = Config('a', 42, unit='')
	b = Config('b', 'foo')
	c = Config('c', 'bar')
	d = Config('d', 'baz')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set b=%a% -r c=%foo% d=%a:02X%')

	assert b.value == '42'
	assert c.value == '%foo%'
	assert d.value == '%a:02X%'

def test_raw_ranger_style() -> None:
	a = Config('a', 42, unit='')
	b = Config('b', 'foo')

	cf = ConfigFile(appname='test')
	cf.set_ui_callback(ui_callback)
	cf.parse_line('set -r b 10%-20%')

	assert b.value == '10%-20%'
