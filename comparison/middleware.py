from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.utils import timezone
from .models import Visitor, VisitorCounter
from datetime import timedelta

class TrackVisitorMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        if ip_address:
            # Check if there's a recent visitor record for this IP address
            recent_visitor = Visitor.objects.filter(
                ip_address=ip_address,
                timestamp__gte=timezone.now() - timedelta(days=1)  # Adjust as needed
            ).exists()

            if not recent_visitor:
                # If no recent visitor, create a new visitor record
                Visitor.objects.create(ip_address=ip_address)

                # Update visitor count if it's a unique visitor
                counter, created = VisitorCounter.objects.get_or_create(pk=settings.VISITOR_COUNTER_ID)
                if created or not recent_visitor:
                    counter.total_visitors = ('total_visitors') + 1
                    counter.save()
        return None  # Explicitly return None for middleware compatibility
