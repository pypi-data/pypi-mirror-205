from ..serializers.base_serializer import BaseSerializer


class CustomSerializer:
    def __init__(self, encoder, serializer: BaseSerializer):
        self._encoder = encoder
        self._serializer = serializer

    def dumps(self, obj):
        return self._serializer.dumps(self._encoder.encode(obj))

    def dump(self, obj, fp):
        return self._serializer.dump(self._encoder.encode(obj), fp)

    def loads(self, s):
        return self._encoder.decode(self._serializer.loads(s))

    def load(self, fp):
        return self._encoder.decode(self._serializer.load(fp))
