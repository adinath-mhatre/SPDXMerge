from datetime import datetime

from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    CreationInfo,
    Document,
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
            spdx_id=self.docnamespace + "#SPDXRef-DOCUMENT",
            name=self.name,
            data_license="CC0-1.0",
            document_namespace=self.docnamespace,
            creators=[Actor(ActorType.PERSON, self.author, self.emailaddr)],
            created=datetime.now(),
        )

        master_doc = Document(creation_info)

        master_doc.packages = []
        for doc in self.doc_list:
            for doc_package in doc.packages:
                if doc_package not in master_doc.packages:
                    master_doc.packages.extend([doc_package])

        master_doc.files = []
        for doc in self.doc_list:
            master_doc.files.extend(doc.files)

        master_doc.snippets = []
        for doc in self.doc_list:
            master_doc.snippets.extend(doc.snippets)

        master_doc.extracted_licensing_info = []
        for doc in self.doc_list:
            master_doc.extracted_licensing_info.extend(doc.extracted_licensing_info)

        master_doc.relationships = []
        for doc in self.doc_list:
            master_doc.relationships.extend(doc.relationships)

        master_doc.annotations = []
        for doc in self.doc_list:
            master_doc.annotations.extend(doc.annotations)

        return master_doc
