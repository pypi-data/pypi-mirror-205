import numpy as np
from pyPhases import classLogger


class NotUniqueException(Exception):
    pass


class NotCompleteException(Exception):
    pass


@classLogger
class DataversionManager:
    def __init__(self, groupedRecords, splits, seed=None) -> None:
        self.splits = splits
        self.seed = seed
        self.removedRecords = {}

        # shuffle the records
        groups = list(groupedRecords.keys())
        if seed is not None:
            np.random.seed(seed)
            np.random.shuffle(groups)
            groupedRecords = {g: groupedRecords[g] for g in groups}

        self.groupedRecords = groupedRecords

    def groupDatasetBySplit(self, datasetName, splits, groupedRecords, removedRecords=None):
        sliceForDataset = slice(*[int(index) for index in splits[datasetName][0].split(":")])
        groups = list(groupedRecords.keys())[sliceForDataset]

        recordIds = [record for group in groups for record in groupedRecords[group]]
        if bool(removedRecords):
            recordIds = [record for index, record in enumerate(recordIds) if index not in removedRecords]

        return recordIds

    def groupDatasetsBySplit(self, datasetNames, splits, groupedRecords):
        recordSlices = {}
        for datasetName in datasetNames:
            recordSlices[datasetName] = self.groupDatasetBySplit(datasetName, splits, groupedRecords)

        return recordSlices

    def getRecordsForSplit(self, datasetName):
        removedRecords = self.removedRecords.get(datasetName, None)
        return self.groupDatasetBySplit(datasetName, self.splits, self.groupedRecords, removedRecords)

    def validatDatasetVersion(self, datasetNames, raiseException=True):
        allDBRecordIds = self.groupedRecords
        splits = self.splits

        recordSlices = self.groupDatasetsBySplit(datasetNames, splits, allDBRecordIds)

        flattenAllRecords = [r for elem in allDBRecordIds.values() for r in elem]
        flattenUsedRecords = [r for elem in recordSlices.values() for r in elem]

        # check if all records are unique and present in the dataset splits
        complete = len(flattenAllRecords) == len(flattenUsedRecords)
        unique = len(flattenUsedRecords) == len(set(flattenUsedRecords))
        if not unique:
            error = "There are duplicate records in the dataset splits "
            self.logError(error)
            if raiseException:
                raise NotUniqueException(error)

        if not complete:
            error = "Not all records are used (%i records are missing), overall %s groups" % (
                len(flattenAllRecords) - len(flattenUsedRecords),
                len(allDBRecordIds.keys()),
            )
            self.logError(error)

            if raiseException:
                raise NotCompleteException(error)

        if complete and unique:
            self.logSuccess("All records are unique and present in the dataset splits")

    def removeRecordIndexesFromSplit(self, datasetName, recordIndexes):
        self.removedRecords[datasetName] = recordIndexes
