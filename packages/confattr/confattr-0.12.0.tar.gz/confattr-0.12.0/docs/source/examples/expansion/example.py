#!../../../../venv/bin/python3

__package__ = 'exampleapp'

# ------- start -------
from confattr import Config, ConfigFile

class App:
	s = Config('s', 'hello world')
	i = Config('i', 42, unit='')
	b = Config('b', True)
a = App()

config_file = ConfigFile(appname=__package__)
config_file.set_ui_callback(print)
# ------- 1 -------
config_file.parse_line('set s = "%i% = 0x%i:02X%"')
assert a.s == '42 = 0x2A'
# ------- 2 -------
config_file.parse_line('set s = "[%b!:<5%] ..."')
assert a.s == '[true ] ...'
# ------- 3 -------
config_file.parse_line('set i = %b:d%')
assert a.i == 1
# ------- 4 -------
config_file.parse_line('set s="i was %i%" i=2 s="%s%, i is %i%"')
assert a.s == 'i was 1, i is 2'
# ------- 5 -------
config_file.parse_line('set s="%i%%%"')
assert a.s == '2%'
# ------- 6 -------
config_file.parse_line('set s="hello ${HELLO:-world}"')
assert a.s == 'hello world'
