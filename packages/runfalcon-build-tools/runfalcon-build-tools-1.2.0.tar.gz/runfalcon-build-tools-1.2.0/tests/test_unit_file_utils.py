import os
from runfalconbuildtools.file_utils import copy_dir, create_dir_if_not_exists, delete_directory, file_exists, get_current_path, touch

def test_file_exist_true_directory():
    assert file_exists('.')

def test_file_exist_true_file():
    assert file_exists(get_current_path() + '/__init__.py')

def test_file_exist_false():
    assert not file_exists('./not-existing-directory-name')

def test_copy_dir():
    test_dir_base:str = './test-of-copy-recursive-dir'
    delete_directory(test_dir_base)
    create_dir_if_not_exists(test_dir_base)
    create_dir_if_not_exists(os.path.join(test_dir_base, 'src/dir_1/dir_1_1'))
    touch(os.path.join(test_dir_base, 'src/dir_1/file1.txt'))
    touch(os.path.join(test_dir_base, 'src/dir_1/dir_1_1/file2.txt'))
    copy_dir(os.path.join(test_dir_base, 'src/dir_1'), os.path.join(test_dir_base, 'target'))
