from runfalconbuildtools.artifacts import ArtifactsManager, DummyArtifact
from runfalconbuildtools.file_utils import file_exists

# def test_download_dummy():
#     manager:ArtifactsManager = ArtifactsManager()
#     output_file:str = manager.get_artifact(DummyArtifact())
#     print('>>>>>> dummy file: {file}'.format(file = output_file))
#     assert file_exists(output_file)

def test_get_artifact():
    manager:ArtifactsManager = ArtifactsManager()
    response = manager.get_artifact_from_code_artifact(\
                            domain='runfalcon', \
                            repository='Runfalcon', \
                            format='maven', \
                            namespace='com.runfalcon.agentreceiver', \
                            package='runfalcon-agent-receiver')

    print(' >>>> Artifact: {}'.format(response))
