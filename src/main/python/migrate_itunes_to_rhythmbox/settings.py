from path import Path
# well, not so easy to get path resolution work during test execution for both a) a single test executed via IDE and b) via pyb
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent  # climb up to project root
TARGET_FOLDER = PROJECT_ROOT.joinpath(PROJECT_ROOT, 'target')
TESTOUTPUT_FOLDER = PROJECT_ROOT.joinpath(TARGET_FOLDER, 'testoutput')
TEST_RESOURCES_FOLDER = PROJECT_ROOT.joinpath(PROJECT_ROOT, 'src', "unittest", "resources")
