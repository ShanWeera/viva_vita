from datetime import datetime
from enum import Enum
from uuid import uuid4

from mongoengine import (
    connect,
    StringField,
    EmbeddedDocumentListField,
    EmbeddedDocumentField,
    QuerySet,
    EnumField,
    DateTimeField,
    EmbeddedDocument,
    ListField,
    FloatField,
    UUIDField,
    IntField,
)
from mongoengine_goodjson import Document, FollowReferenceField

from ..settings import ResourceConfig

settings = ResourceConfig()

connect(
    host=settings.mongo_host,
    username=settings.mongo_ddm_username,
    password=settings.mongo_ddm_password,
    port=27017,
    db=settings.mongo_ddm_database,
    authentication_source=settings.mongo_ddm_database,
)


class LoggerMessages(Enum):
    PROSITE_STARTING = 'Prosite analysis is starting.'
    PROSITE_RUNNING = 'Prosite analysis is running.'
    PROSITE_ERROR = 'Prosite analysis failed.'
    PROSITE_COMPLETED = 'Prosite analysis completed.'

    BLAST_STARTING = 'Blast analysis is starting.'
    BLAST_RUNNING = 'Blast analysis is running.'
    BLAST_ERROR = 'Blast analysis failed.'
    BLAST_COMPLETED = 'Blast analysis completed.'

    MHCI_STARTING = 'MHCI prediction is starting.'
    MHCI_RUNNING = 'MHCI prediction is running.'
    MHCI_ERROR = 'MHCI prediction failed.'
    MHCI_COMPLETED = 'MHCI prediction completed.'

    MHCII_STARTING = 'MHCII prediction is starting.'
    MHCII_RUNNING = 'MHCII prediction is running.'
    MHCII_ERROR = 'MHCII prediction failed.'
    MHCII_COMPLETED = 'MHCII prediction completed.'


class LoggerContexts(Enum):
    blast: str = 'blast'
    prosite: str = 'prosite'
    mhci: str = 'mhci'
    mhcii: str = 'mhcii'


class MHCIPredictionMethods(Enum):
    NETMHCPAN_EL: str = "netmhcpan_el"
    NETMHCPAN: str = "netmhcpan"
    PICKPOCKET: str = "pickpocket"
    MHCFLURRY: str = 'mhcflurry'


class MHCIIPredictionMethods(Enum):
    NETMHCIIPAN: str = "NetMHCIIpan"
    NETMHCPAN_EL: str = "netmhciipan_el"
    NETMHCPAN_BA: str = "netmhciipan_ba"


class LoggerFlags(Enum):
    info: str = 'info'
    error: str = 'error'
    warning: str = 'warning'


class HCSStatuses(Enum):
    pending: str = 'pending'
    start: str = 'start'
    running: str = 'running'
    completed: str = 'completed'
    failed: str = 'failed'


class LoggerQuerySet(QuerySet):
    def update_log(self, context: LoggerContexts, flag: LoggerFlags, msg: LoggerMessages):
        entry = LogEntryDBModel(flag=flag, message=msg)
        hcs = self.get()

        if context == LoggerContexts.blast:
            hcs.logs.blast.append(entry)
        elif context == LoggerContexts.prosite:
            hcs.logs.prosite.append(entry)

        hcs.logs.save()
        hcs.save()


class LogEntryDBModel(EmbeddedDocument):
    id = UUIDField(required=True, default=uuid4, binary=False, db_field='id')
    flag = EnumField(LoggerFlags, required=True)
    timestamp = DateTimeField(required=True, default=datetime.now)
    message = EnumField(LoggerMessages, required=True)


class LogsDBModel(Document):
    prosite = EmbeddedDocumentListField(LogEntryDBModel, required=False)
    blast = EmbeddedDocumentListField(LogEntryDBModel, required=False)
    mhci = EmbeddedDocumentListField(LogEntryDBModel, required=False)
    mhcii = EmbeddedDocumentListField(LogEntryDBModel, required=False)

    meta = {'collection': 'logs'}


class StepStatusesDBModel(EmbeddedDocument):
    prosite = EnumField(HCSStatuses, default=HCSStatuses.pending)
    blast = EnumField(HCSStatuses, default=HCSStatuses.pending)
    mhci = EnumField(HCSStatuses, default=HCSStatuses.pending)
    mhcii = EnumField(HCSStatuses, default=HCSStatuses.pending)


class PrositeDBModel(EmbeddedDocument):
    accession = StringField(required=True, max_length=12)
    description = StringField(required=True)
    start = IntField(required=True)
    end = IntField(required=True)


class BlastDBModel(EmbeddedDocument):
    accession = StringField(required=True, max_length=12)
    species = StringField(required=True)
    strain = StringField(required=True, null=True)
    taxid = IntField(required=True)
    title = StringField(required=True)


class EpitopeDBModel(EmbeddedDocument):
    allele = StringField(required=True)
    sequence = StringField(required=True)
    percentile = IntField(required=True)


class MHCIISupertypes(EmbeddedDocument):
    DR = EmbeddedDocumentListField(EpitopeDBModel, required=False)
    DP = EmbeddedDocumentListField(EpitopeDBModel, required=False)
    DQ = EmbeddedDocumentListField(EpitopeDBModel, required=False)


class MHCISupertypes(EmbeddedDocument):
    A1 = EmbeddedDocumentListField(EpitopeDBModel, required=False)
    A2 = EmbeddedDocumentListField(EpitopeDBModel, required=False)
    A3 = EmbeddedDocumentListField(EpitopeDBModel, required=False)
    A24 = EmbeddedDocumentListField(EpitopeDBModel, required=False)
    A26 = EmbeddedDocumentListField(EpitopeDBModel, required=False)
    B7 = EmbeddedDocumentListField(EpitopeDBModel, required=False)
    B8 = EmbeddedDocumentListField(EpitopeDBModel, required=False)
    B27 = EmbeddedDocumentListField(EpitopeDBModel, required=False)
    B39 = EmbeddedDocumentListField(EpitopeDBModel, required=False)
    B44 = EmbeddedDocumentListField(EpitopeDBModel, required=False)
    B58 = EmbeddedDocumentListField(EpitopeDBModel, required=False)
    B62 = EmbeddedDocumentListField(EpitopeDBModel, required=False)


class HCSResultsDBModel(EmbeddedDocument):
    prosite = EmbeddedDocumentListField(PrositeDBModel, required=False)
    blast = EmbeddedDocumentListField(BlastDBModel, required=False)
    mhci = EmbeddedDocumentField(MHCISupertypes, required=False)
    mhcii = EmbeddedDocumentListField(MHCIISupertypes, required=False)


class HCSDBModel(Document):
    sequence = StringField(required=True)
    incidence = FloatField(required=True)
    position = IntField(required=True)
    results = EmbeddedDocumentField(HCSResultsDBModel, required=True, default=HCSResultsDBModel())
    status = EmbeddedDocumentField(StepStatusesDBModel, required=True, default=StepStatusesDBModel())
    logs = FollowReferenceField(LogsDBModel, required=False, default=LogsDBModel().save())
    mhci_prediction_method = EnumField(MHCIPredictionMethods, default=MHCIPredictionMethods.NETMHCPAN)
    mhcii_prediction_method = EnumField(MHCIIPredictionMethods, default=MHCIIPredictionMethods.NETMHCIIPAN)

    meta = {'queryset_class': LoggerQuerySet, 'collection': 'hcs'}


class JobDBModel(Document):
    id = StringField(required=True, default=lambda: str(uuid4()), primary_key=True)
    taxonomy_id = IntField(required=True)
    protein_name = StringField(required=True)
    hcs = ListField(FollowReferenceField(HCSDBModel), required=True)

    meta = {'collection': 'job'}
