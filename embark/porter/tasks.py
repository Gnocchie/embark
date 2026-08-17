from celery import shared_task

from porter.exporter import export_results


@shared_task
def export_analysis(analysis_id, export_options):
    """
    Create an EMBArk export archive for an analysis.

    :param analysis_id: ID of the FirmwareAnalysis
    :param export_options: Selected export components
    :return: Path to the generated ZIP archive
    """
    return export_results(
        analysis_id,
        export_options,
    )