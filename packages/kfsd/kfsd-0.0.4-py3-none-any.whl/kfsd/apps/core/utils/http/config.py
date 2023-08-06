from kfsd.apps.core.common.configuration import Configuration


class Config:
    def __init__(self, request):
        self.__request = request

    def getConfigData(self):
        return self.__request.config.getFinalConfig()

    def findConfigs(self, paths):
        return Configuration.findConfigValues(
            self.getConfigData(),
            paths
        )
