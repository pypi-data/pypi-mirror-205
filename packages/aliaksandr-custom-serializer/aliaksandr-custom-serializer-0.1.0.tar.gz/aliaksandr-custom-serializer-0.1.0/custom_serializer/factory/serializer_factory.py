from .custom_serializer import CustomSerializer
from ..encoder.encoder import Encoder
from ..serializers import JsonSerializer, XmlSerializer
from typing import Literal


class SerializerFactory:
    _serializers_map = {
        "json": JsonSerializer,
        "xml": XmlSerializer,
    }

    @classmethod
    def create_serializer(cls, serializer_type: Literal["json", "xml"]):
        serializer = cls._serializers_map.get(serializer_type)

        if serializer is None:
            raise Exception(f"No such serializer format: {serializer_type}")

        return CustomSerializer(Encoder, serializer())
