from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauth.models import User
from django.utils.html import mark_safe

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Location(models.Model):
    lid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="lo")
    location = models.CharField(max_length=50)

    def __str__(self):
        return self.location
    
class Event(models.Model):
    eid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ev")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # For logged-in users
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path)
    description = models.TextField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="events")
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    tickets_sold = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Events"
        ordering = ["date"]
    
    def event_image(self):
        return mark_safe('<img src="/media/%s" />' % (self.image.url))

    def __str__(self):
        return f"{self.title} - {self.location.location}"

    def available_tickets(self):
        return self.capacity - self.tickets_sold
    
    def total_revenue(self):
        return self.tickets_sold * self.ticket_price

class EventImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # For logged-in users
    images = models.ImageField(upload_to=user_directory_path)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Event Images"

class Cart(models.Model):
    # session_key = models.CharField(max_length=100, blank=True, null=True)  # For anonymous users
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)  # For logged-in users
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Cart: {self.user if self.user else self.session_key} - {self.event.title}"

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.quantity}"

