from enum import Enum
from lifeomic_logging import scoped_logger

from ruamel.yaml import YAML
from ingestion.nextgen.util.process_cnv import process_cnv
from ingestion.nextgen.util.process_manifest import process_manifest
from ingestion.nextgen.util.process_structural import process_structural
from ingestion.nextgen.util.process_vcf import process_vcf


def process(
    account_id: str,
    vendor_files: dict,
    local_output_dir: str,
    source_file_id: str,
    prefix: str,
    phc_output_dir: str = ".lifeomic/nextgen",
) -> None:
    with scoped_logger(__name__) as log:
        cnv_path_name = process_cnv(
            pdf_in_file=vendor_files["pdfFile"],
            root_path=local_output_dir,
            prefix=prefix,
            log=log,
        )
        manifest = process_manifest(
            pdf_in_file=vendor_files["pdfFile"],
            source_file_id=source_file_id,
            vendor_files=vendor_files,
            log=log,
        )
        structural_path_name = process_structural(
            pdf_in_file=vendor_files["pdfFile"],
            root_path=local_output_dir,
            prefix=prefix,
            log=log,
        )
        somatic_vcf_meta_data = process_vcf(
            vcf_in_file=vendor_files["somaticVcfFile"],
            root_path=local_output_dir,
            prefix=prefix,
            sequence_type="somatic",
            log=log,
        )
        germline_vcf_meta_data = process_vcf(
            vcf_in_file=vendor_files["germlineVcfFile"],
            root_path=local_output_dir,
            prefix=prefix,
            sequence_type="germline",
            log=log,
        )

    manifest["files"] = [
        {"fileName": cnv_path_name, "sequenceType": "somatic", "type": "copyNumberVariant"},
        {"fileName": structural_path_name, "sequenceType": "somatic", "type": "structuralVariant"},
        {
            "fileName": somatic_vcf_meta_data["vcf_path_name"],
            "sequenceType": "somatic",
            "type": "shortVariant",
        },
        {
            "fileName": germline_vcf_meta_data["vcf_path_name"],
            "sequenceType": "germline",
            "type": "shortVariant",
        },
    ]

    manifest_path_name = f"{local_output_dir}/{prefix}.ga4gh.genomics.yml"
    log.info(f"Saving file to {manifest_path_name}")
    with open(manifest_path_name, "w") as file:
        yaml = YAML()
        yaml.dump(manifest, file)

    return {
        "cnv_path_name": cnv_path_name,
        "manifest_path_name": manifest_path_name,
        "structural_path_name": structural_path_name,
        "somatic_vcf_meta_data": somatic_vcf_meta_data,
        "germline_vcf_meta_data": germline_vcf_meta_data,
    }
