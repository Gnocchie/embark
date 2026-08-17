from celery import shared_task

from porter.exporter import export_results
from porter.models import AnalysisExport
from uploader.models import FirmwareAnalysis


@shared_task
def export_analysis(analysis_id, export_options):
    """
    Create an EMBArk export archive for an analysis.

    :param analysis_id: ID of the FirmwareAnalysis
    :param export_options: Selected export components
    :return: Path to the generated ZIP archive
    """
    analysis = FirmwareAnalysis.objects.get(id=analysis_id)

    export = AnalysisExport.objects.create(
        analysis=analysis,
        export_options=export_options,
        file_path="",
    )

    try:
        zip_path = export_results(
            analysis_id,
            export_options,
            export.id,
        )

        export.file_path = str(zip_path)
        export.save(update_fields=["file_path"])

        return str(zip_path)

    except Exception:
        # Don't leave a database entry for an export that failed.
        export.delete()
        raise