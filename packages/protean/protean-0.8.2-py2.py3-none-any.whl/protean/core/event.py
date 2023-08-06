import logging

from protean.container import BaseContainer, OptionsMixin
from protean.utils import DomainObjects, derive_element_class

logger = logging.getLogger("protean.event")


class BaseEvent(BaseContainer, OptionsMixin):  # FIXME Remove OptionsMixin
    """Base Event class that all Events should inherit from.

    Core functionality associated with Events, like timestamping, are specified
    as part of the base Event class.
    """

    element_type = DomainObjects.EVENT

    class Meta:
        abstract = True


def domain_event_factory(element_cls, **kwargs):
    return derive_element_class(element_cls, BaseEvent)
