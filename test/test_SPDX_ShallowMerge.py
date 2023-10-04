from spdxmerge.SPDX_ShallowMerge import SPDX_ShallowMerger

from datetime import datetime
from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    ChecksumAlgorithm,
    CreationInfo,
    Document,
    SpdxNoAssertion
)
from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID


class Test_SPDX_ShallowMerger:
    def setup_method(self):
        creation_info_1 = CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id=DOCUMENT_SPDX_ID,
            name="Test document 1",
            data_license="CC0-1.0",
            document_namespace="http://example.com/spdx",
            creators=[Actor(ActorType.PERSON, "John Smith", "john@example.com")],
            created=datetime.now(),
            document_comment = "comment1",
        )
        doc1 = Document(creation_info_1)

        creation_info_2 = CreationInfo(
            spdx_version="SPDX-2.3",
            spdx_id=DOCUMENT_SPDX_ID,
            name="Test document 2",
            data_license="CC0-1.0",
            document_namespace="http://example.com/spdx",
            creators=[Actor(ActorType.PERSON, "John Smith", "john@example.com")],
            created=datetime.now(),
            document_comment = "comment2",
        )
        doc2 = Document(creation_info_2)

        self.docs = [doc1,doc2]
        self.m = SPDX_ShallowMerger(doc_list=self.docs, docnamespace="http://example.com/spdx",
                                    name="Test document", author="John Doe")

    def test_document(self):
        doc = self.m.create_document()

        assert doc.creation_info.name == "Test document"
        assert doc.creation_info.spdx_version == "SPDX-2.3"
        assert doc.creation_info.spdx_id == DOCUMENT_SPDX_ID
        assert doc.creation_info.document_namespace == "http://example.com/spdx"
        assert doc.creation_info.data_license == "CC0-1.0"
        assert len(doc.creation_info.creators) == 1
        assert doc.creation_info.creators[0].name == "John Doe"

        assert len(doc.packages) == 1
        package = doc.packages[0]
        assert package.name == "Test document"
        assert package.version == "1.0"
        assert isinstance(package.download_location, SpdxNoAssertion)
        assert len(doc.creation_info.external_document_refs) == 2
        assert doc.creation_info.external_document_refs[0].document_uri == "http://example.com/spdx"
        assert doc.creation_info.external_document_refs[0].checksum.algorithm == ChecksumAlgorithm.SHA1
        assert doc.creation_info.external_document_refs[0].checksum.value == "comment1"
        assert doc.creation_info.external_document_refs[1].document_uri == "http://example.com/spdx"
        assert doc.creation_info.external_document_refs[1].checksum.algorithm == ChecksumAlgorithm.SHA1
        assert doc.creation_info.external_document_refs[1].checksum.value == "comment2"
