from runfalconbuildtools.aws_client import AWSClient, AWSCommandParams

def test_push():
    aws_params:AWSCommandParams = AWSCommandParams(account=462223625310, zone='us-east-1')
    client:AWSClient = AWSClient(aws_params)
    client.push_image_to_ecr(source_image='the_tag:latest', repository='runfalcon-test-repository')

def test_get_ecr_image_info():
    repository:str='runfalcon-load-agent-web-api-stage'
    image_tag:str='runfalcon-load-agent-web-api-latest'
    client:AWSClient = AWSClient()
    data = client.get_ecr_image_data(repository, image_tag)
    print(' >>>> {}'.format(data))
    print(' >>>> ' + data["imageDigest"])
    assert  data != None

def test_get_latest_version():
    client:AWSClient = AWSClient()
    latest_version:str = client.get_artifact_latest_version(\
                            domain='runfalcon', \
                            repository='Runfalcon', \
                            format='maven', \
                            namespace='com.runfalcon.agentreceiver', \
                            package='runfalcon-agent-receiver')
    print(' >>>>> Latest version: {}'.format(latest_version))
    assert latest_version != None

def test_get_artifact():
    client:AWSClient = AWSClient()
    response = client.get_from_artifacts(\
                        domain='runfalcon', \
                        repository='Runfalcon', \
                        format='maven', \
                        namespace='com.runfalcon.agentreceiver', \
                        package='runfalcon-agent-receiver', \
                        package_version='1.0.10')

    print (' >>>> Artifact downloaded: {}'.format(response))
