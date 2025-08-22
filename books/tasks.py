from celery import shared_task
from django.db.models import F
from .models import Author

@shared_task(bind=True)
def bump_author_age(author_id=None):

    if author_id:
        updated = Author.objects.filter(id=author_id).update(yas=F("yas") + 1)
        return {"updated_count": updated, "scope": "single", "author_id": author_id}
    else:
        updated = Author.objects.update(yas=F("yas") + 1)
        return {"updated_count": updated, "scope": "all"}
