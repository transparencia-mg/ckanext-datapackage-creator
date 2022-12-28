import datetime as dt
import uuid
import logging

from sqlalchemy import Column, Unicode, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON

from ckan.model.meta import metadata

log = logging.getLogger(__name__)


def make_uuid():
    return str(uuid.uuid4())


Base = declarative_base(metadata=metadata)


class Datapackage(Base):
    __tablename__ = u'datapackage'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    package_id = Column(Unicode)
    status = Column(Unicode, default=u'created')
    created = Column(DateTime, default=dt.datetime.utcnow)
    data = Column(JSON)
    errors = Column(JSON)


class DatapackageResource(Base):
    __tablename__ = u'datapackage_resource'

    id = Column(Unicode, primary_key=True, default=make_uuid)
    resource_id = Column(Unicode)
    status = Column(Unicode, default=u'created')
    created = Column(DateTime, default=dt.datetime.utcnow)
    data = Column(JSON)
    errors = Column(JSON)


def create_tables():
    Datapackage.__table__.create()
    DatapackageResource.__table__.create()
