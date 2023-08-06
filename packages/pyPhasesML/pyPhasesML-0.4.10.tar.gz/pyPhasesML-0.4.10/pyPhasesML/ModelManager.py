import importlib

from pyPhases import ConfigNotFoundException

from .Model import Model


class ModelManager:
    model: Model = None
    modelOptions = None
    beforeBuild = None
    modelPath = None

    @staticmethod
    def getModel(forceReload=False) -> Model:
        if ModelManager.model is None or forceReload:
            if ModelManager.modelOptions is None:
                raise Exception("ModelManager setModel was never called!")
            else:
                ModelManager.loadModelFromOptions()
        return ModelManager.model

    def loadModelFromOptions() -> None:
        options = ModelManager.modelOptions
        modelClass = ModelManager.loadModelByModule(options["modelName"])
        model = modelClass(options["modelConfig"])

        for field in options["general"]:
            setattr(model, field, options["general"][field])

        if ModelManager.beforeBuild is not None:
            ModelManager.beforeBuild(model)

        model.init()
        model.define()
        model.build()
        ModelManager.model = model

    def validate(config):
        def checkValueInConfig(config, value, valuePath=None):
            checkDict = config if valuePath is None else config[valuePath]

            if value not in checkDict:
                valuePath = value if valuePath is None else valuePath + "." + value
                raise ConfigNotFoundException("The value '%s' is required in the config" % valuePath)

        checkValueInConfig(config, "modelName")
        checkValueInConfig(config, "classification")
        checkValueInConfig(config, "trainingParameter")
        checkValueInConfig(config, "inputShape")
        checkValueInConfig(config, "classNames", "classification")
        checkValueInConfig(config, "batchSize", "trainingParameter")

        if not isinstance(config["classification"]["classNames"], list):
            raise ConfigNotFoundException("The value 'classification.classNames' is required to be a list of class names")

    @staticmethod
    def loadModel(project) -> None:
        config = project.config
        ModelManager.validate(config)
        ModelManager.modelPath = config["modelPath"]

        trainingParameter = config["trainingParameter"]
        classNames = config["classification"]["classNames"]
        classCount = len(classNames)
        ModelManager.modelOptions = {
            "modelName": project.config["modelName"],
            "modelConfig": project.getConfig("model", {}),
            "general": {
                "inputShape": project.config["inputShape"],
                "numClasses": classCount,
                "maxEpochs": project.getConfig("trainingParameter.maxEpochs", None, False),
                "batchSize": trainingParameter["batchSize"],
                "classWeights": project.getConfig("trainingParameter.classWeights", None, False),
                "classNames": classNames,
                "learningRate": project.getConfig("trainingParameter.learningRate", 0.001),
                "learningRateDecay": project.getConfig("trainingParameter.learningRateDecay", None, False),
                "stopAfterNotImproving": project.getConfig("trainingParameter.stopAfterNotImproving", 10),
                "validationEvery": project.getConfig("trainingParameter.validationEvery", None, False),
                "optimizer": project.getConfig("trainingParameter.optimizer", "Adams"),
                "ignoreClassIndex": project.getConfig("ignoreClassIndex", None, False),
                "validationMetrics": project.getConfig("trainingParameter.validationMetrics", ["loss"]),
                "useEventScorer": project.getConfig("trainingParameter.useEventScorer", False),
                "predictionType": project.getConfig("classification.type", "classification"),
                "oneHotDecoded": project.getConfig("oneHotDecoded", False),
            },
        }

    @staticmethod
    def loadModelByModule(name):
        path = ModelManager.modelPath.replace("/", ".")
        packageSplit = path.split(".")
        package = packageSplit[0]
        path = ".".join(packageSplit[1:])
        path = "." + path if path != "" else ""
        module = importlib.import_module("%s.%s.%s" % (path, name, name), package)
        # module = importlib.import_module(".%s.%s" % (name, name), package=userModels.__package__)
        return getattr(module, name)
