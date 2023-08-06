
from runfalconbuildtools.aws_client import AWSClient

class SSLCertificateManager:

    __ssl_cetificates_bucket__:str = 'runfalcon-ssl-certs'

    def download_certificates(self, application:str, environment:str, out_dir:str) -> any:
        aws_client:AWSClient = AWSClient()
        s3_url:str = 's3://{bucket_name}/{env}/{application}'.format( \
            bucket_name = self.__ssl_cetificates_bucket__, \
            env = environment, \
            application = application \
        )
        aws_client.get_from_s3(s3_url, out_dir, True)

