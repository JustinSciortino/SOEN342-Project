from .SpaceType import SpaceType
from .SpecializationType import SpecializationType

SPACE_SPECIALIZATION_MAP = {
    SpaceType.rink: [SpecializationType.hockey],
    SpaceType.field: [SpecializationType.soccer, SpecializationType.football],
    SpaceType.gym: [SpecializationType.gym, SpecializationType.basketball],
    SpaceType.studio: [SpecializationType.yoga, SpecializationType.dance],
    SpaceType.pool: [SpecializationType.swim],
    SpaceType.court: [SpecializationType.basketball],
    SpaceType.track: [SpecializationType.running],
}