from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from accounts.scoring import update_user_score


@receiver(post_save, sender="accounts.User")
def manage_trusted_user_permissions(sender, instance, created, **kwargs):
    """
    Automatically grant/remove approval permissions based on trusted status.
    """
    if created:
        return

    try:
        # Get the content types for the models we need permissions for
        from busstops.models import DataChangeLog
        from vehicles.models import VehicleRevision
        from service_requests.models import Request

        busstops_content_type = ContentType.objects.get_for_model(DataChangeLog)
        vehicles_content_type = ContentType.objects.get_for_model(VehicleRevision)
        service_requests_content_type = ContentType.objects.get_for_model(Request)

        # Approval permissions to manage
        approval_permissions = [
            Permission.objects.get(
                codename='approve_datachangelog',
                content_type=busstops_content_type
            ),
            Permission.objects.get(
                codename='reject_datachangelog',
                content_type=busstops_content_type
            ),
            Permission.objects.get(
                codename='approve_vehiclerevision',
                content_type=vehicles_content_type
            ),
            Permission.objects.get(
                codename='approve_request',
                content_type=service_requests_content_type
            ),
            Permission.objects.get(
                codename='reject_request',
                content_type=service_requests_content_type
            ),
            Permission.objects.get(
                codename='change_request_status',
                content_type=service_requests_content_type
            ),
            Permission.objects.get(
                codename='approve_photo_request',
                content_type=service_requests_content_type
            ),
            Permission.objects.get(
                codename='approve_vehicle_request',
                content_type=service_requests_content_type
            ),
            Permission.objects.get(
                codename='approve_service_request',
                content_type=service_requests_content_type
            ),
            Permission.objects.get(
                codename='approve_vehicle_type_request',
                content_type=service_requests_content_type
            ),
            Permission.objects.get(
                codename='approve_operator_request',
                content_type=service_requests_content_type
            ),
        ]

        if instance.trusted:
            # Grant approval permissions if not already granted
            for permission in approval_permissions:
                if not instance.user_permissions.filter(id=permission.id).exists():
                    instance.user_permissions.add(permission)
        else:
            # Remove approval permissions
            for permission in approval_permissions:
                instance.user_permissions.remove(permission)
    except Exception as e:
        # Silently fail if models or permissions don't exist yet
        pass


@receiver(post_save, sender="vehicles.VehicleRevision")
def update_score_on_revision_save(sender, instance, created, **kwargs):
    """
    Update user score when a revision is saved (created or updated).
    """
    if instance.user:
        update_user_score(instance.user)


@receiver(post_delete, sender="vehicles.VehicleRevision")
def update_score_on_revision_delete(sender, instance, **kwargs):
    """
    Update user score when a revision is deleted.
    """
    if instance.user:
        update_user_score(instance.user)


@receiver(post_save, sender="vehicles.VehicleReview")
def update_score_on_review_save(sender, instance, created, **kwargs):
    """
    Update user score when a review is saved (created or updated).
    """
    if instance.user:
        update_user_score(instance.user)


@receiver(post_delete, sender="vehicles.VehicleReview")
def update_score_on_review_delete(sender, instance, **kwargs):
    """
    Update user score when a review is deleted.
    """
    if instance.user:
        update_user_score(instance.user)
