import os
import yaml
import datetime
import unittest
from unittest import mock
from yaml_env_tag import construct_env_tag

def mockenv(**kwargs):
    ''' Decorator to mock os.environ with provided variables. '''
    return mock.patch.dict(os.environ, kwargs)


class TestYamlEnvTag(unittest.TestCase):

    def assertYamlLoad(self, data, expected, loader=yaml.Loader):
        loader.add_constructor('!ENV', construct_env_tag)
        self.assertEqual(expected, yaml.load(data, Loader=loader))

    @mockenv(VAR='foo')
    def test_scalar(self):
        self.assertYamlLoad(
            '!ENV VAR',
            'foo'
        )

    def test_scalar_undefined(self):
        self.assertYamlLoad(
            '!ENV VAR',
            None
        )

    @mockenv(VAR='foo')
    def test_safe_loader(self):
        self.assertYamlLoad(
            '!ENV VAR',
            'foo',
            yaml.SafeLoader
        )

    @mockenv(VAR='foo')
    def test_scalar_in_squence(self):
        self.assertYamlLoad(
            '- !ENV VAR',
            ['foo']
        )

    @mockenv(VAR='foo')
    def test_scalar_in_mapping(self):
        self.assertYamlLoad(
            'key: !ENV VAR',
            {'key': 'foo'}
        )

    @mockenv(VAR='foo')
    def test_sequence_1(self):
        self.assertYamlLoad(
            '!ENV [VAR]',
            'foo'
        )

    def test_sequence_1_undefined(self):
        self.assertYamlLoad(
            '!ENV [VAR]',
            None
        )

    @mockenv(VAR='foo')
    def test_sequence_2(self):
        self.assertYamlLoad(
            '!ENV [VAR, default]',
            'foo'
        )

    def test_sequence_2_undefined(self):
        self.assertYamlLoad(
            '!ENV [VAR, default]',
            'default'
        )

    @mockenv(VAR1='foo', VAR2='bar')
    def test_sequence_3(self):
        self.assertYamlLoad(
            '!ENV [VAR1, VAR2, default]',
            'foo'
        )

    @mockenv(VAR2='bar')
    def test_sequence_3_1_undefined(self):
        self.assertYamlLoad(
            '!ENV [VAR1, VAR2, default]',
            'bar'
        )

    def test_sequence_3_undefined(self):
        self.assertYamlLoad(
            '!ENV [VAR1, VAR2, default]',
            'default'
        )

    def test_default_type_null(self):
        self.assertYamlLoad(
            '!ENV [VAR, null]',
            None
        )

    def test_default_type_tilde(self):
        self.assertYamlLoad(
            '!ENV [VAR, ~]',
            None
        )

    def test_default_type_bool_false(self):
        self.assertYamlLoad(
            '!ENV [VAR, false]',
            False
        )

    def test_default_type_bool_true(self):
        self.assertYamlLoad(
            '!ENV [VAR, true]',
            True
        )

    def test_default_type_str(self):
        self.assertYamlLoad(
            '!ENV [VAR, "a string"]',
            'a string'
        )

    def test_default_type_int(self):
        self.assertYamlLoad(
            '!ENV [VAR, 42]',
            42
        )

    def test_default_type_float(self):
        self.assertYamlLoad(
            '!ENV [VAR, 3.14]',
            3.14
        )

    def test_default_type_date(self):
        self.assertYamlLoad(
            '!ENV [VAR, 2020-11-11]',
            datetime.date(2020, 11, 11)
        )

    def test_default_type_sequence(self):
        self.assertYamlLoad(
            '!ENV [VAR, [foo, bar]]',
            ['foo', 'bar']
        )

    def test_default_type_mapping(self):
        self.assertYamlLoad(
            '!ENV [VAR, foo: bar]',
            {'foo': 'bar'}
        )

    @mockenv(VAR='null')
    def test_env_value_type_null(self):
        self.assertYamlLoad(
            '!ENV [VAR, default]',
            None
        )

    @mockenv(VAR='~')
    def test_env_value_type_tilde(self):
        self.assertYamlLoad(
            '!ENV [VAR, default]',
            None
        )

    @mockenv(VAR='false')
    def test_env_value_type_bool_false(self):
        self.assertYamlLoad(
            '!ENV VAR',
            False
        )

    @mockenv(VAR='true')
    def test_env_value_type_bool_true(self):
        self.assertYamlLoad(
            '!ENV VAR',
            True
        )

    @mockenv(VAR='a string')
    def test_env_value_type_str(self):
        self.assertYamlLoad(
            '!ENV VAR',
            'a string'
        )

    @mockenv(VAR='42')
    def test_env_value_type_int(self):
        self.assertYamlLoad(
            '!ENV VAR',
            42
        )

    @mockenv(VAR='3.14')
    def test_env_value_type_float(self):
        self.assertYamlLoad(
            '!ENV VAR',
            3.14
        )

    @mockenv(VAR='2020-11-11')
    def test_env_value_type_date(self):
        self.assertYamlLoad(
            '!ENV VAR',
            datetime.date(2020, 11, 11)
        )

    @mockenv(VAR='[foo, bar]')
    def test_env_value_type_sequence(self):
        self.assertYamlLoad(
            '!ENV VAR',
            '[foo, bar]'
        )

    @mockenv(VAR='foo: bar')
    def test_env_value_type_mapping(self):
        self.assertYamlLoad(
            '!ENV VAR',
            'foo: bar'
        )

    @mockenv(UPPERCASE='foo')
    def test_env_name_uppercase(self):
        self.assertYamlLoad(
            '!ENV UPPERCASE',
            'foo'
        )

    @mockenv(lowercase='foo')
    def test_env_name_lowercase(self):
        self.assertYamlLoad(
            '!ENV lowercase',
            'foo'
        )

    @mockenv(CamelCase='foo')
    def test_env_name_CamelCase(self):
        self.assertYamlLoad(
            '!ENV CamelCase',
            'foo'
        )

    @mockenv(snake_case='foo')
    def test_env_name_snake_case(self):
        self.assertYamlLoad(
            '!ENV snake_case',
            'foo'
        )

    # WARNING! The Environment Variable names in the following tests are
    # probably a bad idea in use. In fact, it may not even be possable to
    # set them in most OSs. We are testing that they don't get converted
    # to native Python types, ensuring expected results in edge cases. 

    @mockenv(null='foo')
    def test_env_name_null(self):
        self.assertYamlLoad(
            '!ENV null',
            'foo'
        )

    @mockenv(**{'~': 'foo'})
    def test_env_name_tilde(self):
        self.assertYamlLoad(
            '!ENV ~',
            'foo'
        )

    @mockenv(**{'true': 'foo'})
    def test_env_name_true(self):
        self.assertYamlLoad(
            '!ENV true',
            'foo'
        )

    @mockenv(**{'false': 'foo'})
    def test_env_name_false(self):
        self.assertYamlLoad(
            '!ENV false',
            'foo'
        )

    @mockenv(**{'42': 'foo'})
    def test_env_name_int(self):
        self.assertYamlLoad(
            '!ENV 42',
            'foo'
        )

    @mockenv(**{'3.14': 'foo'})
    def test_env_name_float(self):
        self.assertYamlLoad(
            '!ENV 3.14',
            'foo'
        )

    @mockenv(**{'2020-11-11': 'foo'})
    def test_env_name_date(self):
        self.assertYamlLoad(
            '!ENV 2020-11-11',
            'foo'
        )

    def test_env_name_sequance(self):
        yaml.Loader.add_constructor('!ENV', construct_env_tag)
        self.assertRaises(
            yaml.constructor.ConstructorError,
            yaml.load, 
            '!ENV [[foo]]', 
            Loader=yaml.Loader
        )

    def test_env_name_mapping(self):
        yaml.Loader.add_constructor('!ENV', construct_env_tag)
        self.assertRaises(
            yaml.constructor.ConstructorError,
            yaml.load, 
            '!ENV {key: value}', 
            Loader=yaml.Loader
        )

if __name__ == '__main__':
    unittest.main()
