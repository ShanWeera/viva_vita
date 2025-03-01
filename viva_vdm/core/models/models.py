from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
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
    JOB_PENDING = 'Job has been created'

    JOB_RUNNING = 'Job is running'
    JOB_ERROR = 'Job failed'

    PROSITE_STARTING = 'Prosite analysis is starting.'
    PROSITE_RUNNING = 'Prosite analysis is running.'
    PROSITE_ERROR = 'Prosite analysis failed: {error}'
    PROSITE_COMPLETED = 'Prosite analysis completed.'

    BLAST_STARTING = 'Blast analysis is starting.'
    BLAST_RUNNING = 'Blast analysis is running.'
    BLAST_ERROR = 'Blast analysis failed: {error}'
    BLAST_COMPLETED = 'Blast analysis completed.'

    MHCI_STARTING = 'MHCI prediction is starting.'
    MHCI_RUNNING = 'MHCI prediction is running.'
    MHCI_ERROR = 'MHCI prediction failed: {error}'
    MHCI_COMPLETED = 'MHCI prediction completed.'

    MHCII_STARTING = 'MHCII prediction is starting.'
    MHCII_RUNNING = 'MHCII prediction is running.'
    MHCII_ERROR = 'MHCII prediction failed: {error}'
    MHCII_COMPLETED = 'MHCII prediction completed.'

    JOB_COMPLETED = 'Job is complete'


class LoggerContexts(Enum):
    blast: str = 'blast'
    prosite: str = 'prosite'
    mhci: str = 'mhci'
    mhcii: str = 'mhcii'
    general: str = 'general'


@dataclass
class LoggerMessageMap:
    pending = {
        LoggerContexts.general: LoggerMessages.JOB_PENDING,
    }

    running = {
        LoggerContexts.prosite: LoggerMessages.PROSITE_RUNNING,
        LoggerContexts.blast: LoggerMessages.BLAST_RUNNING,
        LoggerContexts.mhci: LoggerMessages.MHCI_RUNNING,
        LoggerContexts.mhcii: LoggerMessages.MHCII_RUNNING,
        LoggerContexts.general: LoggerMessages.JOB_RUNNING,
    }

    starting = {
        LoggerContexts.prosite: LoggerMessages.PROSITE_STARTING,
        LoggerContexts.blast: LoggerMessages.BLAST_STARTING,
        LoggerContexts.mhci: LoggerMessages.MHCI_STARTING,
        LoggerContexts.mhcii: LoggerMessages.MHCII_STARTING,
    }

    error = {
        LoggerContexts.prosite: LoggerMessages.PROSITE_ERROR,
        LoggerContexts.blast: LoggerMessages.BLAST_ERROR,
        LoggerContexts.mhci: LoggerMessages.MHCI_ERROR,
        LoggerContexts.mhcii: LoggerMessages.MHCII_ERROR,
        LoggerContexts.general: LoggerMessages.JOB_ERROR,
    }

    completed = {
        LoggerContexts.prosite: LoggerMessages.PROSITE_COMPLETED,
        LoggerContexts.blast: LoggerMessages.BLAST_COMPLETED,
        LoggerContexts.mhci: LoggerMessages.MHCI_COMPLETED,
        LoggerContexts.mhcii: LoggerMessages.MHCII_COMPLETED,
        LoggerContexts.general: LoggerMessages.JOB_COMPLETED,
    }


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


class JobStatuses(Enum):
    pending: str = 'pending'
    starting: str = 'starting'
    started: str = 'started'
    partial: str = 'partial'
    completed: str = 'completed'
    error: str = 'failed'


class JobDBModel:
    ...


class LoggerQuerySet(QuerySet):
    def update_log(
        self,
        *,
        context: LoggerContexts,
        flag: LoggerFlags,
        msg: LoggerMessages,
        instance: Optional[JobDBModel] = None,
        pk: Optional[str] = None,
    ):
        if not instance and not pk:
            raise ValueError('Either an instance, or a pk needed')

        entry = LogEntryDBModel(flag=flag, message=msg, context=context)
        job = instance or self.get(id=pk)

        job.logs.append(entry)
        job.save()

        return job

    def update_status(self, *, status: JobStatuses, instance: Optional[JobDBModel] = None, pk: Optional[str] = None):
        if not instance and not pk:
            raise ValueError('Either an instance, or a pk needed')

        job = instance or self.get(id=pk)

        job.status = status
        job.save()


class LogEntryDBModel(EmbeddedDocument):
    id = UUIDField(required=True, default=uuid4, binary=False, db_field='id')
    flag = EnumField(LoggerFlags, required=True)
    context = EnumField(LoggerContexts, required=True)
    timestamp = DateTimeField(required=True, default=datetime.now)
    message = EnumField(LoggerMessages, required=True)

    meta = {'collection': 'logs'}


class PrositeDBModel(EmbeddedDocument):
    accession = StringField(required=True, max_length=12)
    description = StringField(required=True)
    start = IntField(required=True)
    end = IntField(required=True)


class BlastDBModel(EmbeddedDocument):
    accession = StringField(required=True, max_length=12)
    species = StringField(null=True, default=None)
    strain = StringField(null=True, default=None)
    taxid = IntField(null=True, default=None)
    title = StringField(required=True)


class EpitopeDBModel(EmbeddedDocument):
    allele = StringField(required=True)
    sequence = StringField(required=True)
    percentile = FloatField(required=True)


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
    mhcii = EmbeddedDocumentField(MHCIISupertypes, required=False)


class HCSDBModel(Document):
    sequence = StringField(required=True)
    incidence = FloatField(required=True)
    position = IntField(required=True)
    results = EmbeddedDocumentField(HCSResultsDBModel, required=True, default=HCSResultsDBModel())

    meta = {'collection': 'hcs'}


class JobDBModel(Document):
    id = StringField(required=True, default=lambda: str(uuid4()), primary_key=True)
    taxonomy_id = IntField(required=True)
    protein_name = StringField(required=True)
    hcs = ListField(FollowReferenceField(HCSDBModel), required=True)
    status = EnumField(JobStatuses, default=JobStatuses.pending)
    logs = EmbeddedDocumentListField(LogEntryDBModel, default=[])
    mhci_prediction_method = EnumField(MHCIPredictionMethods, default=MHCIPredictionMethods.NETMHCPAN)
    mhcii_prediction_method = EnumField(MHCIIPredictionMethods, default=MHCIIPredictionMethods.NETMHCIIPAN)

    meta = {'collection': 'job', 'queryset_class': LoggerQuerySet}
