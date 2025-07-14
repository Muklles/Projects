from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Bid, Listing, Comment

def index(request):
    ListingsActive = Listing.objects.filter(isActive=True)
    categories = Category.objects.all()  
    return render(request, "auctions/index.html",{
        "listings": ListingsActive,
        "categories": categories, 
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import Category, Listing

def create(request):
    if request.method == 'GET':
        # Info about the form.
        categories = Category.objects.all()  
        return render(request, "auctions/create.html", {
            "categories": categories  
        })
    elif request.method == 'POST':
        # Info about the form.
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["imageURL"]
        price = request.POST["price"]
        category_name = request.POST["category"] 
        # Whos submiting the form.
        current_user = request.user
        # Finding the correct instance of the Category model based on the received name.
        category_instance = Category.objects.get(category=category_name)
        # Creating a new bid object.
        bid = Bid.objects.create(bid=int(price), user=current_user)
        bid.save()
        # New form.
        new_listing = Listing.objects.create(
            title=title,
            description=description,
            imageURL=image,
            price=bid,
            category=category_instance,  
            Listing_User=current_user,
        )
        # Saving the new form.
        new_listing.save()
        # Redirecting to index.
        return HttpResponseRedirect(reverse('index'))

def listing(request, id):
    listingInfo = Listing.objects.get(pk=id)
    ListingWatchList = request.user in listingInfo.watchlist.all()
    Comments = Comment.objects.filter(listing=listingInfo)
    ifitsOwner = request.user.username == listingInfo.Listing_User.username
    return render(request, "auctions/listing.html", {
        "listing": listingInfo,
        "ListingWatchList": ListingWatchList,
        "comments": Comments,
        "ifitsOwner": ifitsOwner,
    })

def display(request):
    if request.method == "POST":
        category_name = request.POST.get('category')
        if category_name == 'all':
            listings_active = Listing.objects.filter(isActive=True)
        else:
            category = Category.objects.get(category=category_name)
            listings_active = Listing.objects.filter(isActive=True, category=category)
        categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": listings_active,
            "categories": categories,
        })

def watchlist(request):
    currentUser = request.user
    listings = currentUser.listingWatchList.all()
    return render(request, "auctions/watchlist.html",{
        "listings":listings
    })

def removewatchlist(request, id):
    listingInfo = Listing.objects.get(pk=id)
    current_user = request.user
    listingInfo.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def addwatchlist(request, id):
    listingInfo = Listing.objects.get(pk=id)
    current_user = request.user
    listingInfo.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id,))) 

def comment(request, id):
    current_user = request.user
    listingInfo = Listing.objects.get(pk=id)
    message = request.POST['comment'] 
    newComment = Comment(
        author=current_user,
        listing=listingInfo,
        message=message,
    )

    newComment.save()

    return HttpResponseRedirect(reverse("listing", args=(id,)))


def bid(request, id):
    if request.method == "POST":
        newBid = float(request.POST.get('bid', 0))
        listingInfo = Listing.objects.get(pk=id)
        ListingWatchList = request.user in listingInfo.watchlist.all()
        Comments = Comment.objects.filter(listing=listingInfo)
        ifitsOwner = request.user.username == listingInfo.Listing_User.username
        if newBid > listingInfo.price.bid:
            updateBid = Bid(user=request.user, bid=newBid)
            updateBid.save()
            listingInfo.price = updateBid
            listingInfo.save()
            message = "Bid was updated"
            update = True
        else:
            message = "Bid must be higher than current bid"
            update = False
        return render(request, "auctions/listing.html", {
            "listing": listingInfo,
            "message": message,
            "update": update,
            "ListingWatchList": ListingWatchList,
            "comments": Comments,
            "ifitsOwner": ifitsOwner,
        })

def closing(request, id):
    listingInfo = Listing.objects.get(pk=id)
    listingInfo.isActive = False
    listingInfo.save()
    ifitsOwner = request.user.username == listingInfo.Listing_User.username
    return render(request, "auctions/listing.html", {
        "listing": listingInfo,
        "ifitsOwner": ifitsOwner,
        "message": "Auction Closed."
    })