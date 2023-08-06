from runfalconbuildtools.main_module import ModuleMain
from runfalconbuildtools.file_utils import delete_directory

BASE_PATH='/Users/raul.devilla/data/RUNFALCON/platform/runfalcon-build-tools-py-package'

def test_download_artifact():
    args = ['aw-artifact', 'get', 'name=apache-jmeter-runfalcon', 'version=1.0.0', 'out=.']
    module_main:ModuleMain = ModuleMain(args)
    module_main.run()

def test_configure_json_file():
    json_file:str = BASE_PATH + '/scripts/test/resources/test_json_config-2.json'
    args = ['config', 'json', 'file={}'.format(json_file), 'param-1="configured value"']
    module_main:ModuleMain = ModuleMain(args)
    module_main.run()

def test_configure_properties_file():
    properties_file:str = BASE_PATH + '/scripts/test/resources/test_properties_config-2.properties'
    args = ['config', 'properties', 'file={}'.format(properties_file), 'param-1="configured value"']
    module_main:ModuleMain = ModuleMain(args)
    module_main.run()

def test_download_config():
    out_dir:str = './test-config'
    delete_directory(out_dir)
    args = ['config', 'download', 'application=runfalcon-load-agent-web-api', 'env=STAGE', 'outdir={}'.format(out_dir)]
    module_main:ModuleMain = ModuleMain(args)
    module_main.run()

def test_get_ssh_public_key():
    out_dir:str = './test-config'
    delete_directory(out_dir)
    args = ['keys', 'get', 'application=runfalcon-load-agent-web-api', 'name=ssh', 'env=STAGE', 'outdir={}'.format(out_dir)]
    module_main:ModuleMain = ModuleMain(args)
    module_main.run()

