from typing import TypeVar, Type, Optional, Dict, List

from .base import BaseImageDataset
from ..network_dataset import NetworkDataset
from ...sample import ImageSample
from ...annotation import ImageDatasetClass, ImageDatasetClasses
from ....codable import KeyDescriptor
from ....networking import NetworkManager, RequestType


DatasetType = TypeVar("DatasetType", bound = "ImageDataset")
SampleType = TypeVar("SampleType", bound = "ImageSample")


class ImageDataset(BaseImageDataset[SampleType], NetworkDataset[SampleType]):  # type: ignore

    """
        Represents the Image Dataset class \n
        Includes functionality for working with Image Datasets
        that are uploaded to Coretex.ai
    """

    @classmethod
    def _keyDescriptors(cls) -> Dict[str, KeyDescriptor]:
        descriptors = super()._keyDescriptors()

        descriptors["samples"] = KeyDescriptor("sessions", ImageSample, list)
        descriptors["classes"] = KeyDescriptor("classes", ImageDatasetClass, ImageDatasetClasses)

        return descriptors

    @classmethod
    def fetchById(cls: Type[DatasetType], objectId: int, queryParameters: Optional[List[str]] = None) -> Optional[DatasetType]:
        obj = super().fetchById(objectId, queryParameters)
        if obj is None:
            return None

        response = NetworkManager.instance().genericJSONRequest(
            endpoint=f"annotation-class?dataset_id={obj.id}",
            requestType=RequestType.get,
        )

        if not response.hasFailed():
            obj.classes = cls._decodeValue("classes", response.json)
            obj._writeClassesToFile()

        return obj

    def saveClasses(self, classes: ImageDatasetClasses) -> bool:
        parameters = {
            "dataset_id": self.id,
            "classes": [clazz.encode() for clazz in classes]
        }

        response = NetworkManager.instance().genericJSONRequest("annotation-class", RequestType.post, parameters)
        if not response.hasFailed():
            return super().saveClasses(classes)

        return not response.hasFailed()
