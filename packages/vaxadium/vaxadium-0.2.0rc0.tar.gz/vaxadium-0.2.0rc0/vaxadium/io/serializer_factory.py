from vaxadium.io.serializers import (
    AttenuatorsSerializer,
    BackgroundSerializer,
    BeamSerializer,
    DataCollectionsSerializer,
    DetectorSerializer,
    DummySerializer,
    Geant4MacrosSerializer,
    PyFAISerializer,
    ScaledExperimentCollectionSerializer,
    SimulationSerializer,
)


class NexusSerializer:
    def serialize(self, serializable, format):
        serializer = factory.get_serializer(format)
        serializable.serialize(serializer)
        return serializer.get()


class SerializerFactory:
    def __init__(self):
        self._creators = {}

    def register_format(self, format, creator):
        self._creators[format.lower()] = creator

    def get_serializer(self, format):
        creator = self._creators[format.lower()]
        if not creator:
            raise ValueError(format)
        return creator()


class SERIALIZERS:
    BEAM = "beam"
    DETECTOR = "detector"
    ATTENUATORS = "attenuators"
    DUMMY = "dummy"
    G4DIFFSIM = "g4diffsim"
    EXPERIMENT = "experiment"
    SIMULATION = "simulation"
    PYFAI = "pyfai"
    DATACOLLECTIONS = "data_collections"
    BACKGROUND = "background"
    SCALEDCOLLECTION = "scaled"


factory = SerializerFactory()
factory.register_format(SERIALIZERS.BEAM, BeamSerializer)
factory.register_format(SERIALIZERS.DETECTOR, DetectorSerializer)
factory.register_format(SERIALIZERS.ATTENUATORS, AttenuatorsSerializer)
factory.register_format(SERIALIZERS.DUMMY, DummySerializer)
factory.register_format(SERIALIZERS.G4DIFFSIM, Geant4MacrosSerializer)
factory.register_format(SERIALIZERS.SIMULATION, SimulationSerializer)
factory.register_format(SERIALIZERS.PYFAI, PyFAISerializer)
factory.register_format(SERIALIZERS.DATACOLLECTIONS, DataCollectionsSerializer)
factory.register_format(SERIALIZERS.BACKGROUND, BackgroundSerializer)
factory.register_format(
    SERIALIZERS.SCALEDCOLLECTION, ScaledExperimentCollectionSerializer
)

nexus_serializer = NexusSerializer()
