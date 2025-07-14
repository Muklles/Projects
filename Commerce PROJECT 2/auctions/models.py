from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="UserBid")


class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category

class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    imageURL = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bidPrice")
    isActive = models.BooleanField(default=True)
    Listing_User = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="User")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="Category")
    watchlist = models.ManyToManyField(User, blank=True, related_name="listingWatchList")
    

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="UserComment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="ListingComment")
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"