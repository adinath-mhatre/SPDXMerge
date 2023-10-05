from datetime import datetime
from uuid import uuid4
from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    Checksum,
    ChecksumAlgorithm,
    CreationInfo,
    Document,
    ExternalDocumentRef,
    Package,
    Relationship,
    RelationshipType,
    SpdxNoAssertion,
)

class SPDX_ShallowMerger():
    def __init__(self,doc_list=None,docnamespace=None,name=None,author=None,email=None):
        self.doc_list = doc_list
        self.docnamespace = docnamespace
        self.name = name
        self.author = author
        self.emailaddr = email

    def create_document(self):
        external_references = []
        for doc in self.doc_list:
            check_sum = Checksum(ChecksumAlgorithm.SHA1,doc.creation_info.document_comment)
            extDoc = ExternalDocumentRef(
                document_ref_id="DocumentRef-" + str(uuid4()),
                document_uri=doc.creation_info.document_namespace,
                checksum=check_sum
            )
            external_references.append(extDoc)

        creation_info = CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id=DOCUMENT_SPDX_ID,
            name=self.name,
            data_license="CC0-1.0",
            document_namespace=self.docnamespace,
            external_document_refs=external_references,
            creators=[Actor(ActorType.PERSON, self.author, self.emailaddr)],
            created=datetime.now(),
        )
        master_doc = Document(creation_info)

        package = Package(
            spdx_id="SPDXRef-package-" + str(uuid4()),
            name=self.name,
            download_location=SpdxNoAssertion(),
        )

        if self.authortype in ["P", "p"]:
            package.supplier = Actor(ActorType.PERSON, self.author, self.emailaddr)
        else:
            package.supplier = Actor(ActorType.ORGANIZATION, self.author, self.emailaddr)

        package.version = "1.0"
        master_doc.packages = [package]

        master_doc.relationships = [Relationship(
            spdx_element_id=master_doc.creation_info.spdx_id,
            relationship_type=RelationshipType.DESCRIBES,
            related_spdx_element_id=package.spdx_id,
        )]

        return master_doc
