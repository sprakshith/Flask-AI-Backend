import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class SystemArchitectAgentPrompts:
    def __init__(self):
        self.SYSTEM_MESSAGE = open(os.path.join(DIR_PATH, 'SystemArchitectAgent/SYSTEM_MESSAGE.prompt'), 'r').read()


class DatabaseArchitectAgentPrompts:
    def __init__(self):
        self.SCHEMA_DESIGN_SYSTEM_MESSAGE = open(os.path.join(DIR_PATH, 'DatabaseArchitectAgent/DesignProjectSchema/SCHEMA_DESIGN_SM.prompt'), 'r').read()
        self.SCHEMA_DESIGN_HUMAN_MESSAGE = open(os.path.join(DIR_PATH, 'DatabaseArchitectAgent/DesignProjectSchema/SCHEMA_DESIGN_HM.prompt'), 'r').read()
        self.SCHEMA_CONTINUATION_HUMAN_MESSAGE = open(os.path.join(DIR_PATH, 'DatabaseArchitectAgent/DesignProjectSchema/SCHEMA_CONTINUATION_HM.prompt'), 'r').read()
        self.MODEL_GENERATION_SYSTEM_MESSAGE = open(os.path.join(DIR_PATH, 'DatabaseArchitectAgent/ModelGeneration/MODEL_GENERATION_SM.prompt'), 'r').read()
        self.MODEL_GENERATION_HUMAN_MESSAGE = open(os.path.join(DIR_PATH, 'DatabaseArchitectAgent/ModelGeneration/MODEL_GENERATION_HM.prompt'), 'r').read()


class BackendDeveloperAgentPrompts:
    def __init__(self):
        self.API_ENDPOINTS_DESIGN_SYSTEM_MESSAGE = open(os.path.join(DIR_PATH, 'BackendDevAgent/DesignEndpoints/API_ENDPOINTS_DESIGN_SM.prompt'), 'r').read()
        self.API_ENDPOINTS_DESIGN_HUMAN_MESSAGE = open(os.path.join(DIR_PATH, 'BackendDevAgent/DesignEndpoints/API_ENDPOINTS_DESIGN_HM.prompt'), 'r').read()
        self.API_ENDPOINTS_GENERATION_SYSTEM_MESSAGE = open(os.path.join(DIR_PATH, 'BackendDevAgent/GenerateEndpoints/API_ENDPOINTS_GENERATION_SM.prompt'), 'r').read()
        self.API_ENDPOINTS_GENERATION_HUMAN_MESSAGE = open(os.path.join(DIR_PATH, 'BackendDevAgent/GenerateEndpoints/API_ENDPOINTS_GENERATION_HM.prompt'), 'r').read()
        self.GENERATE_REQUIREMENTS_SYSTEM_MESSAGE = open(os.path.join(DIR_PATH, 'BackendDevAgent/GenerateRequirementsFile/GENERATE_REQUIREMENTS_SM.prompt'), 'r').read()
        self.GENERATE_REQUIREMENTS_HUMAN_MESSAGE = open(os.path.join(DIR_PATH, 'BackendDevAgent/GenerateRequirementsFile/GENERATE_REQUIREMENTS_HM.prompt'), 'r').read()


class FrontendDeveloperAgentPrompts:
    def __init__(self):
        self.FRONTEND_DESIGN_SYSTEM_MESSAGE = open(os.path.join(DIR_PATH, 'FrontendDevAgent/DesignFrontend/FRONTEND_DESIGN_SM.prompt'), 'r').read()
        self.FRONTEND_DESIGN_HUMAN_MESSAGE = open(os.path.join(DIR_PATH, 'FrontendDevAgent/DesignFrontend/FRONTEND_DESIGN_HM.prompt'), 'r').read()
        self.GENERATE_HTML_SYSTEM_MESSAGE = open(os.path.join(DIR_PATH, 'FrontendDevAgent/GenerateHTML/GENERATE_HTML_SM.prompt'), 'r').read()
        self.GENERATE_HTML_HUMAN_MESSAGE = open(os.path.join(DIR_PATH, 'FrontendDevAgent/GenerateHTML/GENERATE_HTML_HM.prompt'), 'r').read()
        self.GENERATE_CSS_SYSTEM_MESSAGE = open(os.path.join(DIR_PATH, 'FrontendDevAgent/GenerateCSS/GENERATE_CSS_SM.prompt'), 'r').read()
        self.GENERATE_CSS_HUMAN_MESSAGE = open(os.path.join(DIR_PATH, 'FrontendDevAgent/GenerateCSS/GENERATE_CSS_HM.prompt'), 'r').read()
        self.GENERATE_JS_SYSTEM_MESSAGE = open(os.path.join(DIR_PATH, 'FrontendDevAgent/GenerateJS/GENERATE_JS_SM.prompt'), 'r').read()
        self.GENERATE_JS_HUMAN_MESSAGE = open(os.path.join(DIR_PATH, 'FrontendDevAgent/GenerateJS/GENERATE_JS_HM.prompt'), 'r').read()
