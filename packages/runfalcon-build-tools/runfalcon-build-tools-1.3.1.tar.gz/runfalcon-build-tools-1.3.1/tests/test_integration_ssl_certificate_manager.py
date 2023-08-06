import array
from runfalconbuildtools.ssl_certificate_manager import SSLCertificateManager

def test_build_image_requiered_para_not_set():

    application:str = 'runfalcon-web-app-api'
    environment:str = 'STAGE'
    out_dir:str = './working_dir'

    ssl_certificate_manager:SSLCertificateManager = SSLCertificateManager()
    ssl_certificate_manager.download_certificates( \
        application = application, \
        environment = environment, \
        out_dir = out_dir \
    )
    
    print(' >>> SSL certificates for "{application}:{env}" downloaded to "{out_dir}".'.format( \
        application = application, \
        env = environment, \
        out_dir = out_dir
    ))
