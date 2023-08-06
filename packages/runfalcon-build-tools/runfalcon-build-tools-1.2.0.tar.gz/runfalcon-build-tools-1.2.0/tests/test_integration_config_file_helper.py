
from runfalconbuildtools.properties import Properties
from runfalconbuildtools.config_files_helper import ConfigFileHelper
from runfalconbuildtools.file_utils import delete_directory
import json

def test_replace_in_json_file():
    config:ConfigFileHelper = ConfigFileHelper()
    in_json_file:str = './scripts/test/resources/test_json_config.json'
    json_out:json = config.set_values_in_json_file( \
            in_json_file, \
            [{"key-1": "new value"}] \
            )
    assert json_out["key-1"] == "new value"


def test_replace_in_propertiesfile():
    config:ConfigFileHelper = ConfigFileHelper()
    in_properties_file:str = './scripts/test/resources/test_properties_config.properties'
    properties_out:Properties = config.set_values_in_properties_file( \
            in_properties_file, \
            [{'key1': 'new value', 'key2': 'new value 2'}]
            )
    print('properties_out : {properties_out}'.format(properties_out = properties_out.to_string()))
    assert properties_out.get('key1') == 'new value'


def test_get_config_from_repo():
    out_dir:str = './test-config'
    delete_directory(out_dir)
    config:ConfigFileHelper = ConfigFileHelper()
    config.get_config_files_from_repo('runfalcon-load-agent-web-api', 'STAGE', out_dir)