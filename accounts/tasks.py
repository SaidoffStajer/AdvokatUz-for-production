from celery import shared_task
from accounts import models


@shared_task(name='delete_used_confirmation_codes')
def delete_used_confirmation_codes():
    deleted_count, _ = models.UserConfirmation.objects.filter(is_used=True).delete()
    return f"{deleted_count} tasdiqlash kodlari o'chirildi."