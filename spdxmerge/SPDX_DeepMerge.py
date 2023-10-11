from datetime import datetime

from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID
from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    CreationInfo,
    Document,
    Relationship,
    RelationshipType,
)

class SPDX_DeepMerger():

    def __init__(self,doc_list=None,docnamespace=None,name=None,author=None,email=None):
        self.doc_list = doc_list
        self.docnamespace = docnamespace
        self.name = name
        self.author = author
        self.emailaddr = email

    def create_document(self):
        creation_info = CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id=DOCUMENT_SPDX_ID,
            name=self.name,
            data_license="CC0-1.0",
            document_namespace=self.docnamespace,
            creators=[Actor(ActorType.PERSON, self.author, self.emailaddr)],
            created=datetime.now(),
        )

        master_doc = Document(creation_info)

        master_doc.packages = []
        master_doc.relationships = []
        for doc in self.doc_list:
            for doc_package in doc.packages:
                if doc_package not in master_doc.packages:
                    master_doc.packages.extend([doc_package])
                    # Add document relationship with package
                    doc_relationship = Relationship(
                        spdx_element_id=DOCUMENT_SPDX_ID,
                        relationship_type=RelationshipType.DESCRIBES,
                        related_spdx_element_id=doc_package.spdx_id,
                    )
                    master_doc.relationships.append(doc_relationship)

        master_doc.files = []
        for doc in self.doc_list:
            master_doc.files.extend(doc.files)

        master_doc.snippets = []
        for doc in self.doc_list:
            master_doc.snippets.extend(doc.snippets)

        master_doc.extracted_licensing_info = []
        for doc in self.doc_list:
            master_doc.extracted_licensing_info.extend(doc.extracted_licensing_info)

        for doc in self.doc_list:
            for new_rel in doc.relationships:
                if new_rel not in master_doc.relationships:
                    master_doc.relationships.append(new_rel)

        master_doc.annotations = []
        for doc in self.doc_list:
            master_doc.annotations.extend(doc.annotations)

        return master_doc
