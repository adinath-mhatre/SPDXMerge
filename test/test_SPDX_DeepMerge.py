from datetime import datetime

from spdxmerge.SPDX_DeepMerge import SPDX_DeepMerger

from spdx_tools.spdx.model import (
    Actor,
    ActorType,
    Annotation,
    AnnotationType,
    Checksum,
    ChecksumAlgorithm,
    CreationInfo,
    Document,
    ExtractedLicensingInfo,
    File,
    Package,
    Relationship,
    RelationshipType,
    Snippet,
    SpdxNoAssertion,
)
from spdx_tools.spdx.constants import DOCUMENT_SPDX_ID

class TestSPDXDeepMerger:

    def test_document(self):
        docs = []
        for idx in range(2):
            # Create documents
            creation_info = CreationInfo(
                spdx_version="SPDX-2.3",
                spdx_id=DOCUMENT_SPDX_ID,
                name="Test document " + str(idx+1),
                data_license="CC0-1.0",
                document_namespace="http://example.com/spdx",
                creators=[Actor(ActorType.PERSON, "John Smith", "john@example.com")],
                created=datetime.now(),
            )
            docs.append(Document(creation_info))

            # Add package information to each document
            package = Package(
                spdx_id="SPDXRef-package-" + str(idx+1),
                name="Package " + str(idx+1),
                download_location=SpdxNoAssertion(),
            )
            docs[idx].packages.append(package)

            # Add file information to each document
            file = File(
                spdx_id="SPDXRef-file-" + str(idx+1),
                name = "File " + str(idx+1),
                checksums = [Checksum(ChecksumAlgorithm.SHA256, "Test_checksum_" + str(idx+1))]
            )
            docs[idx].files.append(file)

            # Add snippet information to each document
            snippet = Snippet(
                spdx_id="SPDXRef-file-" + str(idx+1),
                file_spdx_id = "File " + str(idx+1),
                byte_range = (8, 16)
            )
            docs[idx].snippets.append(snippet)

            # Add extracted licensing information to each document
            extracted_licensing_info = ExtractedLicensingInfo(license_name="License_" + str(idx+1))
            docs[idx].extracted_licensing_info.append(extracted_licensing_info)

            # Add relationship information to each document
            docs[idx].relationships.append(Relationship(
                spdx_element_id=docs[idx].creation_info.spdx_id,
                relationship_type=RelationshipType.DESCRIBES,
                related_spdx_element_id=docs[idx].packages[0].spdx_id
                )
            )

            # Add annotation information to each document
            annotation = Annotation(
                spdx_id="SPDXRef-annotation-" + str(idx+1),
                annotation_type=AnnotationType.REVIEW,
                annotator=Actor(ActorType.PERSON, "John Smith", "john@example.com"),
                annotation_date=datetime.now(),
                annotation_comment="Comment " + str(idx+1)
            )
            docs[idx].annotations.append(annotation)

        # Add package DEPENDS_ON relationship
        docs[0].relationships.append(Relationship(
            spdx_element_id=docs[0].packages[0].spdx_id,
            relationship_type=RelationshipType.DEPENDS_ON,
            related_spdx_element_id=docs[1].packages[0].spdx_id
            )
        )

        # Merge the two documents using SPDX_DeepMerger
        merger = SPDX_DeepMerger(doc_list=docs, docnamespace="https://example.com", name="Test Document",
                                 authortype="O", author="Test Author")
        merge_doc = merger.create_document()

        # Verify that the merged document
        assert merge_doc.creation_info.name == "Test Document"
        assert merge_doc.creation_info.spdx_version == "SPDX-2.3"
        assert merge_doc.creation_info.spdx_id == DOCUMENT_SPDX_ID
        assert merge_doc.creation_info.document_namespace == "https://example.com"
        assert merge_doc.creation_info.data_license == "CC0-1.0"
        assert len(merge_doc.creation_info.creators) == 1
        assert merge_doc.creation_info.creators[0].actor_type == ActorType.ORGANIZATION
        assert merge_doc.creation_info.creators[0].name == "Test Author"

        assert len(merge_doc.packages) == 2
        assert merge_doc.packages[0].name == "Package 1"
        assert merge_doc.packages[1].name == "Package 2"

        assert len(merge_doc.files) == 2
        assert merge_doc.files[0].name == "File 1"
        assert merge_doc.files[0].checksums[0].algorithm == ChecksumAlgorithm.SHA256
        assert merge_doc.files[0].checksums[0].value == "Test_checksum_1"
        assert merge_doc.files[1].name == "File 2"
        assert merge_doc.files[1].checksums[0].algorithm == ChecksumAlgorithm.SHA256
        assert merge_doc.files[1].checksums[0].value == "Test_checksum_2"

        assert len(merge_doc.snippets) == 2
        assert merge_doc.snippets[0].file_spdx_id == "File 1"
        assert merge_doc.snippets[0].byte_range == (8, 16)
        assert merge_doc.snippets[1].file_spdx_id == "File 2"
        assert merge_doc.snippets[1].byte_range == (8, 16)

        assert len(merge_doc.extracted_licensing_info) == 2
        assert merge_doc.extracted_licensing_info[0].license_name == "License_1"
        assert merge_doc.extracted_licensing_info[1].license_name == "License_2"

        assert len(merge_doc.relationships) == 3
        assert merge_doc.relationships[0].relationship_type == RelationshipType.DESCRIBES
        assert merge_doc.relationships[0].spdx_element_id == docs[0].creation_info.spdx_id
        assert merge_doc.relationships[0].related_spdx_element_id == docs[0].packages[0].spdx_id

        assert merge_doc.relationships[1].relationship_type == RelationshipType.DEPENDS_ON
        assert merge_doc.relationships[1].spdx_element_id == docs[0].packages[0].spdx_id
        assert merge_doc.relationships[1].related_spdx_element_id == docs[1].packages[0].spdx_id

        assert merge_doc.relationships[2].relationship_type == RelationshipType.DESCRIBES
        assert merge_doc.relationships[2].spdx_element_id == docs[1].creation_info.spdx_id
        assert merge_doc.relationships[2].related_spdx_element_id == docs[1].packages[0].spdx_id

        assert len(merge_doc.annotations) == 2
        assert merge_doc.annotations[0].spdx_id == "SPDXRef-annotation-1"
        assert merge_doc.annotations[0].annotation_type == AnnotationType.REVIEW
        assert merge_doc.annotations[0].annotator.name == "John Smith"
        assert merge_doc.annotations[0].annotation_comment == "Comment 1"
        assert merge_doc.annotations[1].spdx_id == "SPDXRef-annotation-2"
        assert merge_doc.annotations[1].annotation_type == AnnotationType.REVIEW
        assert merge_doc.annotations[1].annotator.name == "John Smith"
        assert merge_doc.annotations[1].annotation_comment == "Comment 2"
