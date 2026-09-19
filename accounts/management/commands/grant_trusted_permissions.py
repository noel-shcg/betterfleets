from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User


class Command(BaseCommand):
    help = 'Grant approval permissions to all trusted users'

    def handle(self, *args, **options):
        try:
            # Get the content types for the models we need permissions for
            from busstops.models import DataChangeLog
            from vehicles.models import VehicleRevision
            from service_requests.models import Request

            busstops_content_type = ContentType.objects.get_for_model(DataChangeLog)
            vehicles_content_type = ContentType.objects.get_for_model(VehicleRevision)
            service_requests_content_type = ContentType.objects.get_for_model(Request)

            # Grant approval permissions
            permissions_to_grant = [
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

            # Get all trusted users
            trusted_users = User.objects.filter(trusted=True)
            count = 0

            for user in trusted_users:
                for permission in permissions_to_grant:
                    user.user_permissions.add(permission)
                count += 1
                self.stdout.write(f'Granted permissions to {user.get_display_name()}')

            self.stdout.write(
                self.style.SUCCESS(f'Successfully granted permissions to {count} trusted users')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error granting permissions: {str(e)}')
            )
