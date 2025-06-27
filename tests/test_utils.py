import pytest
from utils.utils import clean_text, load_yaml, load_json

def test_clean_text():
    assert clean_text('  Hello   world\n') == 'Hello world'

def test_load_yaml():
    config = load_yaml('utils/config.yaml')
    assert 'keywords' in config
    assert isinstance(config['keywords'], list)

def test_load_json(tmp_path):
    data = {'a': 1}
    file = tmp_path / 'test.json'
    file.write_text('{"a": 1}', encoding='utf-8')
    loaded = load_json(str(file))
    assert loaded['a'] == 1 