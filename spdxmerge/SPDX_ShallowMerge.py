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

TOOL_NAME = "SPDXMerge"

class SPDX_ShallowMerger():
    def __init__(self,doc_list=None,docnamespace=None,name=None,version=None,
                 authortype=None,author=None,email=None):
        self.doc_list = doc_list
        self.docnamespace = docnamespace
        self.name = name
        self.version = version
        self.authortype = authortype
        self.author = author
        self.emailaddr = email

    def create_document(self):
        if self.authortype in ["P", "p"]:
            author=Actor(ActorType.PERSON, self.author, self.emailaddr)
        else:
            author=Actor(ActorType.ORGANIZATION, self.author, self.emailaddr)

        tool = Actor(ActorType.TOOL, TOOL_NAME, None)

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
            name=f"{self.version}-{self.name}-shallow-merge",
            data_license="CC0-1.0",
            document_namespace=self.docnamespace,
            external_document_refs=external_references,
            creators=[author, tool],
            created=datetime.now(),
        )
        master_doc = Document(creation_info)

        package = Package(
            spdx_id=f"SPDXRef-{self.version}-{self.name}",
            name=f"{self.version}-{self.name}",
            download_location=SpdxNoAssertion(),
            files_analyzed=False
        )

        if self.authortype in ["P", "p"]:
            package.supplier = Actor(ActorType.PERSON, self.author, self.emailaddr)
        else:
            package.supplier = Actor(ActorType.ORGANIZATION, self.author, self.emailaddr)

        package.version = self.version
        master_doc.packages = [package]

        master_doc.relationships = [Relationship(
            spdx_element_id=master_doc.creation_info.spdx_id,
            relationship_type=RelationshipType.DESCRIBES,
            related_spdx_element_id=package.spdx_id,
        )]

        return master_doc
