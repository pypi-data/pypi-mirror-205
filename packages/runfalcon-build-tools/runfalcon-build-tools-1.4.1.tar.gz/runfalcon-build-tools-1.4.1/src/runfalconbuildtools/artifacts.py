from abc import ABC, abstractmethod
from enum import Enum
from runfalconbuildtools.aws_client import AWSClient
from runfalconbuildtools.file_utils import file_exists, get_runfalcon_tmp_dir
from runfalconbuildtools.command_line_executor import CommandLineExecutor
from runfalconbuildtools.logger import Logger
from runfalconbuildtools.properties import Properties

LATEST_VERSION:str = 'latest'
UNKNOWN:str = 'unknown'

class Artifact(ABC):
    
    def __init__(self, name:str, type:str):
        self.name = name
        self.type = type

class S3ArtifactMetadata:

    def __init__(self, folder:str, name:str, latest_version:str, type:str):
        self.folder = folder
        self.name = name
        self.latest_version = latest_version
        self.type = type

    def to_simple_file_name(self) -> str:
        return  self.name + \
                ('-' + self.latest_version if self.latest_version != None and self.latest_version != LATEST_VERSION else '') + \
                '.' + (self.type if self.type != None else UNKNOWN)

    def to_s3_resource_url(self) -> str:
        return  (self.folder + '/' if self.folder != None else '') + \
                self.to_simple_file_name()


class S3Artifact(Artifact):

    def __init__(self, name:str, type:str = None, version:str = None):
        super().__init__(name, 'AWS-S3-{}'.format(type))
        self.ext = type
        self.version = version

    def get_simple_name(self):
        return self.name + ('-' + self.version if self.version != None else '') + '.' + (self.ext if self.ext != None else UNKNOWN)

    def get_full_name(self):
        return self.name + '/' + self.get_simple_name()

    def is_latest_version(self) -> bool:
        return self.version == None or self.version == LATEST_VERSION

    def get_metadata(self) -> S3ArtifactMetadata:
        return S3ArtifactMetadata(self.name, self.name, self.version, self.ext)


class JmeterArtifact(S3Artifact):

    def __init__(self, version: str = None):
        super().__init__('jmeter', 'zip', version)

class DummyArtifact(S3Artifact):

    def __init__(self, version: str = None):
        super().__init__('dummy', 'txt', version)

class ArtifactsManager:

    __artifacts_repository_bucket__ = 'runfalcon-repository'
    __logger:Logger = Logger('ArtifactsManager')

    def __get_s3_artifact_url(self, metadata:S3ArtifactMetadata) -> str:
        artifact_url:str = 's3://{bucket}/{artifact}' \
                                .format( \
                                    bucket = self.__artifacts_repository_bucket__, \
                                    artifact = metadata.to_s3_resource_url())
        return artifact_url

    def __get_artifact_metadata__(self, artifact:S3Artifact) -> S3ArtifactMetadata:
        metadata:S3ArtifactMetadata = S3ArtifactMetadata(artifact.name, 'metadata', None, 'txt')

        output_folder:str =  get_runfalcon_tmp_dir()

        self.__logger.info('Downloading metadata for {resource} to {out_folder} ...'.format(resource = metadata.to_s3_resource_url(), out_folder = output_folder))

        aws_client:AWSClient = AWSClient()
        aws_client.get_from_s3(self.__get_s3_artifact_url(metadata), output_folder)

        props:Properties = Properties()
        props.load(output_folder + '/' + metadata.to_simple_file_name())
        latest_version:str = props.get('latest-version')
        
        artifact_metadata:S3ArtifactMetadata = artifact.get_metadata()
        
        if artifact.is_latest_version():
            artifact_metadata.latest_version = latest_version

        artifact_metadata.type = props.get('artifact-type')

        return artifact_metadata


    def __download_artiact_from_aws_s3(self, artifact:S3Artifact) -> str:
        metadata:S3ArtifactMetadata = self.__get_artifact_metadata__(artifact)
        output_folder:str = get_runfalcon_tmp_dir()
        s3_url:str = self.__get_s3_artifact_url(metadata)

        aws_client:AWSClient = AWSClient()
        aws_client.get_from_s3(s3_url, output_folder)

        return output_folder + '/' + metadata.to_simple_file_name()

    def get_artifact(self, artifact:Artifact) -> str:
        if isinstance(artifact, S3Artifact):
            return self.__download_artiact_from_aws_s3(artifact)
        return None

    def get_artifact_from_code_artifact(self, domain:str, repository:str, format:str, namespace:str, package:str, package_version:str = None, out_dir:str = '.', asset:str = None):

        aws_client:AWSClient = AWSClient()
        local_package_version:str = package_version

        if (local_package_version == None):
            local_package_version = aws_client.get_artifact_latest_version(\
                                            domain=domain, \
                                            repository=repository, \
                                            format=format, \
                                            namespace=namespace, \
                                            package=package)

        self.__logger.info('Downloading {namespace}:{package}:{package_version}:{format} from {domain}:{repository} to {out_dir} ...'.format( \
                            namespace=namespace, \
                            package_version=local_package_version, \
                            package=package, \
                            format=format, \
                            domain=domain, \
                            repository=repository, \
                            out_dir=out_dir \
                            ))

        response = aws_client.get_from_artifacts( \
                        domain=domain, \
                        repository=repository, \
                        format=format, \
                        namespace=namespace, \
                        package=package, \
                        package_version=local_package_version,
                        asset=asset, \
                        out_dir=out_dir)

        return response

