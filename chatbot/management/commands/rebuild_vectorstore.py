import logging
from django.core.management.base import BaseCommand
from chatbot.views_upload import build_vectorstore

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Rebuild the Chroma vectorstore from documents in S3 bucket"

    def handle(self, *args, **options):
        logger.info("Rebuilding vectorstore...")

        try:
            vectorstore = build_vectorstore()
            num_vectors = len(vectorstore.get()['ids'])

            self.stdout.write(self.style.SUCCESS(
                f"Vectorstore rebuilt successfully. {num_vectors} vectors stored"
            ))

        except Exception as e:
            logger.error(f"Error rebuilding vectorstore: {e}", exc_info=True)
            self.stderr.write(self.style.ERROR(
                f"Failed to rebuild vectorstore: {e}"
            ))



