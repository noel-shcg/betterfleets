from django.core.management.base import BaseCommand
from django.conf import settings
from photos.models import Photo
import requests


class Command(BaseCommand):
    help = "Refresh all Flickr images by re-downloading them from Flickr URLs"

    def add_arguments(self, parser):
        parser.add_argument(
            '--api',
            action='store_true',
            help='Use Flickr API instead of HTML scraping for higher quality images',
        )
        parser.add_argument(
            '--photo-id',
            type=str,
            help='Only refresh a specific photo by ID',
        )

    def handle(self, *args, **options):
        use_api = options.get('api', False)
        photo_id = options.get('photo_id')

        if use_api and not settings.FLICKR_API_KEY:
            self.stdout.write(
                self.style.ERROR('FLICKR_API_KEY is not set in settings. Please set it to use API mode.')
            )
            return

        # Build queryset
        queryset = Photo.objects.filter(flickr_url__isnull=False).exclude(flickr_url='')
        if photo_id:
            queryset = queryset.filter(id=photo_id)

        total_count = queryset.count()
        if total_count == 0:
            self.stdout.write(self.style.WARNING('No photos with Flickr URLs found.'))
            return

        self.stdout.write(f'Found {total_count} photos with Flickr URLs to refresh.')
        self.stdout.write(f'Mode: {"Flickr API" if use_api else "HTML scraping"}')
        self.stdout.write('')

        success_count = 0
        error_count = 0

        for i, photo in enumerate(queryset, 1):
            self.stdout.write(f'[{i}/{total_count}] Processing photo {photo.id}...')
            
            try:
                if use_api:
                    self.refresh_with_api(photo)
                else:
                    self.refresh_with_scraping(photo)
                
                photo.save()
                success_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Successfully refreshed photo {photo.id}'))
            except Exception as e:
                error_count += 1
                self.stdout.write(self.style.ERROR(f'  ✗ Failed to refresh photo {photo.id}: {str(e)}'))

        self.stdout.write('')
        self.stdout.write(f'Refresh complete: {success_count} succeeded, {error_count} failed')

    def refresh_with_api(self, photo):
        """Refresh photo using Flickr API for higher quality images."""
        import hashlib
        from django.core.files.base import ContentFile
        
        # Extract photo ID from Flickr URL
        # URL format: https://www.flickr.com/photos/{user_id}/{photo_id}/
        try:
            photo_id = photo.flickr_url.split('/photos/', 1)[1].split('/')[1]
        except (IndexError, AttributeError):
            raise ValueError('Could not extract photo ID from Flickr URL')

        session = requests.Session()
        session.params = {
            "format": "json",
            "api_key": settings.FLICKR_API_KEY,
            "photo_id": photo_id,
            "nojsoncallback": 1,
        }

        # Get photo info
        info_response = session.get(
            "https://api.flickr.com/services/rest",
            params={"method": "flickr.photos.getInfo"},
        )
        info_response.raise_for_status()
        info = info_response.json()

        if 'photo' not in info:
            raise ValueError('Invalid response from Flickr API')

        # Update metadata if available
        if 'urls' in info['photo'] and 'url' in info['photo']['urls']:
            photo.url = info['photo']['urls']['url'][0]['_content']
        
        if 'owner' in info['photo']:
            photo.credit = (
                info['photo']['owner'].get('realname') or 
                info['photo']['owner'].get('username', '')
            )
        
        if 'title' in info['photo']:
            photo.caption = info['photo']['title']['_content']

        # Get available sizes
        sizes_response = session.get(
            "https://api.flickr.com/services/rest",
            params={"method": "flickr.photos.getSizes"},
        )
        sizes_response.raise_for_status()
        sizes = sizes_response.json()

        if 'sizes' not in sizes or 'size' not in sizes['sizes']:
            raise ValueError('Could not get photo sizes from Flickr API')

        # Get the largest available size (usually the last one in the list)
        available_sizes = sizes['sizes']['size']
        largest_size = available_sizes[-1]
        image_url = largest_size['source']

        # Download the image
        image_response = session.get(image_url)
        image_response.raise_for_status()

        # Save the image
        filename = hashlib.sha1(image_response.content).hexdigest() + '.jpg'
        photo.image.save(filename, ContentFile(image_response.content), save=False)

    def refresh_with_scraping(self, photo):
        """Refresh photo using HTML scraping (existing method)."""
        # Store the current image to delete it later
        old_image = photo.image
        old_image_name = photo.image.name if photo.image else None
        
        # Re-download from Flickr using the existing method
        if photo.flickr_url:
            photo.download_from_flickr()
            
            # Delete the old image file if it exists and is different
            if old_image_name and old_image_name != photo.image.name:
                try:
                    old_image.delete(save=False)
                except Exception:
                    # Ignore errors when deleting old image
                    pass