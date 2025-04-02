import requests
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import *
from .models import *
from django.http import JsonResponse







# Create your views here.
def home(request):
    return render(request,'Home.html')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("login")
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration.html", {"form": form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful! Welcome back.")
                return redirect('home')  # Redirect to home page
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})

def online_food(request):
    veg_items = FoodItem.objects.filter(category='veg')
    non_veg_items = FoodItem.objects.filter(category='non_veg')
    snack_items = FoodItem.objects.filter(category='snack')
    drinks_items = FoodItem.objects.filter(category='drink')
    context = {
        'veg_items': veg_items,
        'non_veg_items': non_veg_items,
        'snack_items': snack_items,
        'drinks_items': drinks_items
    }
    return render(request,'online_food.html',context)



@login_required
def food_item_detail(request, food_id):
    food_item = get_object_or_404(FoodItem, id=food_id)
    in_cart = Cart.objects.filter(user=request.user, food_item=food_item).exists()
    
    context = {
        'food_item': food_item,
        'in_cart': in_cart
    }
    # Check if the food item is a drink
    if food_item.category.lower() == "drink":
        return render(request, "drink_detail.html", context)
    return render(request, "food_detail.html", context)


def restaurant(request):
    restaurants = Restaurant.objects.exclude(id=None)
    return render(request, 'Restaurant.html', {'restaurants': restaurants})


# def music(request):
#     return render(request,'Music.html')

def music_events(request):
    events = MusicEvent.objects.all()
    return render(request, 'Music.html', {'events': events})

def veg(request):
    veg_items = FoodItem.objects.filter(category='veg')
    return render(request, 'veg.html', {'veg_items': veg_items})
def non_veg(request):
    items = FoodItem.objects.filter(category='non_veg')
    return render(request, 'non-veg.html', {'non_veg_items': items})
def snacks(request):
    items = FoodItem.objects.filter(category__in=['snack', 'drink'])
    return render(request, 'snacks.html', {'snack_items': items})

@login_required
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')  # Redirect to the success page
    else:
        form = ContactForm()
    return render(request, 'Home.html', {'form': form})

def contact_success_view(request):
    return render(request, 'contact_success.html')

@login_required
def add_to_cart(request, food_id):
    food_item = get_object_or_404(FoodItem, id=food_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, food_item=food_item)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.food_item.price * item.quantity for item in cart_items)
    cart_count=cart_items.count()
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price,'cart_count':cart_count})


def increase_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')


def decrease_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # Remove from cart if quantity is 0
    return redirect('cart_view')


def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

@login_required
def cart_count_api(request):
    cart_count = Cart.objects.filter(user=request.user).count()
    return JsonResponse({"cart_count": cart_count})



from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from .models import Cart, Order, OrderItem
from django.utils.html import strip_tags

@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Please add items before placing an order.")
        return redirect('cart_view')

    # ✅ Calculate total price
    total_price = sum(item.food_item.price * item.quantity for item in cart_items)

    # ✅ Create an Order object
    order = Order.objects.create(user=request.user, total_price=total_price)

    # ✅ Create OrderItems and prepare order details
    order_details = "Order Summary:\n"
    order_details += "---------------------------------\n"
    
    for item in cart_items:
        OrderItem.objects.create(order=order, food_item=item.food_item, quantity=item.quantity)
        item_total = item.food_item.price * item.quantity
        order_details += f"{item.food_item.name} × {item.quantity} = ₹{item_total}\n"

    order_details += "---------------------------------\n"
    order_details += f"Total Price: ₹{total_price}\n"

    # ✅ Clear the cart after placing the order
    cart_items.delete()

    # ✅ Prepare Email Content
    subject = f"🎉 Order Confirmation - #{order.id}"
    html_message = f"""
     <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
        <h2 style="color: #ff6f00; text-align: center;">🍽️ Foodie Fiesta Hub</h2>
        
        <div style="background-color: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);">
            <h3 style="color: #28a745;">✅ Order Confirmed!</h3>
            
            <p>Hello <strong style="color: #007bff;">{request.user.username}</strong>,</p>
            
            <p>Thank you for ordering with <strong style="color: #ff6f00;">Foodie Fiesta Hub</strong>! 🍕🌮</p>

            <hr style="border: 1px dashed #ddd;">


    <p><strong>🆔 Order ID:</strong> <span style="color: #dc3545;">#{order.id}</span></p>
    <p><strong>💰 Total Price:</strong> <span style="color: #28a745;">₹{order.total_price}</span></p>
    <hr style="border: 1px dashed #ddd;">


    <h4 style="color: #007bff;">📜 Order Summary:</h4>
    <pre style="background-color: #f1f1f1; padding: 10px; border-radius: 5px; color: #333;">{order_details}</pre>
    <hr style="border: 1px dashed #ddd;">

    <p>We hope you enjoy your meal! 🍔</p>

    <p>🛵 <strong style="color: #17a2b8;">Your order is being prepared and will be on its way soon!</strong></p>

    <p>If you have any questions, feel free to contact us.</p>

    <p style="color: #6c757d; font-size: 14px;"><strong>Bon Appétit! 🍔🍜</strong></p>
    </div>

    <p style="text-align: center; font-size: 12px; color: #888;">© 2025 Foodie Fiesta Hub. All rights reserved.</p>
    </div>
    """

    plain_message = strip_tags(html_message)
    recipient_list = [request.user.email]

    try:
        send_mail(subject,plain_message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message,fail_silently=False)
        messages.success(request, "Your order has been placed successfully! A confirmation email has been sent.")
    except Exception as e:
        messages.error(request, f"Your order was placed, but we couldn't send a confirmation email. Error: {str(e)}")

    return redirect('home')


def order_success(request):
    return render(request, 'order_success.html') 

@login_required
def book_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.restaurant = restaurant
            booking.save()
             # Prepare Email Content
            subject = f"🎉 Booking Confirmation - {restaurant.name}"
            html_message = f"""
            <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
                <h2 style="color: #ff6f00; text-align: center;">🍽️ Foodie Fiesta Hub</h2>
                
                <div style="background-color: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);">
                    <h3 style="color: #28a745;">✅ Booking Confirmed!</h3>
                    
                    <p>Hello <strong style="color: #007bff;">{request.user.username}</strong>,</p>
                    
                    <p>Thank you for booking with <strong style="color: #ff6f00;">Foodie Fiesta Hub</strong>! 🍕🌮</p>

                    <hr style="border: 1px dashed #ddd;">

                    <p><strong>🆔 Booking ID:</strong> <span style="color: #dc3545;">#{booking.id}</span></p>
                    <p><strong>📍 Restaurant:</strong> <span style="color: #007bff;">{restaurant.name}</span></p>
                    <p><strong>📅 Date:</strong> <span style="color: #28a745;">{booking.date}</span></p>
                    <p><strong>🕒 Time:</strong> <span style="color: #28a745;">{booking.time}</span></p>
                    <hr style="border: 1px dashed #ddd;">

                    <p>We hope you enjoy your meal! 🍔</p>

                    <p>🛵 <strong style="color: #17a2b8;">Your table is reserved and we look forward to serving you!</strong></p>

                    <p>If you have any questions, feel free to contact us.</p>

                    <p style="color: #6c757d; font-size: 14px;"><strong>Bon Appétit! 🍔🍜</strong></p>
                </div>

                <p style="text-align: center; font-size: 12px; color: #888;">© 2025 Foodie Fiesta Hub. All rights reserved.</p>
            </div>
            """
            plain_message = strip_tags(html_message)
            recipient_list = [request.user.email]

            try:
                send_mail(subject, plain_message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message, fail_silently=False)
                messages.success(request, "Your booking has been placed successfully! A confirmation email has been sent.")
            except Exception as e:
                messages.error(request, f"Your booking was placed, but we couldn't send a confirmation email. Error: {str(e)}")

            return redirect('restaurant_success', restaurant_id=restaurant_id)
    else:
        form = BookingForm()

    return render(request, 'book_restaurant.html', {'form': form, 'restaurant': restaurant})

def booking_success(request,restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    return render(request, 'booking_success.html',{'restaurant':restaurant})

@login_required
def book_show(request):
    if request.method == "POST":
        form = ShowBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()

            # Prepare Email Content
            subject = f"🎉 Show Booking Confirmation - {booking.show_name}"
            html_message = f"""
            <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f8f9fa; border-radius: 10px;">
                <h2 style="color: #ff6f00; text-align: center;">🎭 Show Booking Confirmation</h2>
                
                <div style="background-color: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);">
                    <h3 style="color: #28a745;">✅ Booking Confirmed!</h3>
                    
                    <p>Hello <strong style="color: #007bff;">{request.user.username}</strong>,</p>
                    
                    <p>Thank you for booking with <strong style="color: #ff6f00;">Foodie Fiesta Hub</strong>! 🎭</p>

                    <hr style="border: 1px dashed #ddd;">

                    <p><strong>🆔 Booking ID:</strong> <span style="color: #dc3545;">#{booking.id}</span></p>
                    <p><strong>🎭 Show:</strong> <span style="color: #007bff;">{booking.show_name}</span></p>
                    <p><strong>📅 Date:</strong> <span style="color: #28a745;">{booking.date}</span></p>
                    <p><strong>🕒 Time:</strong> <span style="color: #28a745;">{booking.time}</span></p>
                    <hr style="border: 1px dashed #ddd;">

                    <p>We hope you enjoy the show! 🎭</p>

                    <p>🛵 <strong style="color: #17a2b8;">Your seats are reserved and we look forward to seeing you!</strong></p>

                    <p>If you have any questions, feel free to contact us.</p>

                    <p style="color: #6c757d; font-size: 14px;"><strong>Enjoy the Show! 🎭</strong></p>
                </div>

                <p style="text-align: center; font-size: 12px; color: #888;">© 2025 Foodie Fiesta Hub. All rights reserved.</p>
            </div>
            """
            plain_message = strip_tags(html_message)
            recipient_list = [request.user.email]

            try:
                send_mail(subject, plain_message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message, fail_silently=False)
                messages.success(request, "Your booking has been placed successfully! A confirmation email has been sent.")
            except Exception as e:
                messages.error(request, f"Your booking was placed, but we couldn't send a confirmation email. Error: {str(e)}")

            return redirect('booking_show_success')  # Redirect to success page
    else:
        form = ShowBookingForm()

    return render(request, 'book_show.html', {'form': form})

def booking_show_success(request):
    return render(request, 'booking_show_success.html')

@login_required
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('home')


def search_view(request):
    query = request.GET.get('q')
    food_results = FoodItem.objects.none()
    restaurant_results = Restaurant.objects.none()
    music_event_results = MusicEvent.objects.none()  # Assuming you have a MusicEvent model
    
    if query:
        food_results = FoodItem.objects.filter(name__icontains=query)
        restaurant_results = Restaurant.objects.filter(name__icontains=query)
        music_event_results = MusicEvent.objects.filter(title__icontains=query)  # Search for music events
    
    context = {
        'food_results': food_results,
        'restaurant_results': restaurant_results,
        'music_event_results': music_event_results,
        'query': query
    }
    
    return render(request, 'search_results.html', context)

def restaurant_view(request):
    query = request.GET.get('q')
    if query:
        restaurants = Restaurant.objects.filter(name__icontains=query)
    else:
        restaurants = Restaurant.objects.all()
    
    context = {
        'restaurants': restaurants,
        'query': query
    }
    
    return render(request, 'Restaurant.html', context)

def food_search_view(request):
    query = request.GET.get('q')
    if query:
        food_items = FoodItem.objects.filter(name__icontains=query)
       
    else:
        food_items = FoodItem.objects.all()
    
    context = {
        'food_items': food_items,
        'query': query
    }
    
    return render(request, 'food_search_results.html', context)

def music_search_view(request):
    query = request.GET.get('q')
    if query:
        events = MusicEvent.objects.filter(title__icontains=query)
    else:
        events = MusicEvent.objects.all()
    
    context = {
        'events': events,
        'query': query
    }
    
    return render(request, 'Music.html', context)


def veg_search_view(request):
    query = request.GET.get('q')
    if query:
        veg_items = FoodItem.objects.filter(name__icontains=query, category='veg')
    else:
        veg_items = FoodItem.objects.filter(category='veg')
    
    context = {
        'veg_items': veg_items,
        'query': query
    }
    
    return render(request, 'veg.html', context)


def non_veg_search_view(request):
    query = request.GET.get('q')
    if query:
        non_veg_items = FoodItem.objects.filter(name__icontains=query, category='non_veg')
    else:
        non_veg_items = FoodItem.objects.filter(category='non_veg')
    
    context = {
        'non_veg_items': non_veg_items,
        'query': query
    }
    
    return render(request, 'non-veg.html', context)

def snacks_drinks_search_view(request):
    query = request.GET.get('q')
    if query:
        snacks_drinks_items = FoodItem.objects.filter(name__icontains=query, category__in=['snack', 'drink'])
    else:
        snacks_drinks_items = FoodItem.objects.filter(category__in=['snack', 'drink'])
    
    context = {
        'snack_items': snacks_drinks_items,
        'query': query
    }
    
    return render(request, 'snacks.html', context)

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileEditForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'edit_profile.html', context)










from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from .forms import CustomPasswordResetForm, CustomSetPasswordForm
from django.contrib.auth import get_user_model

User = get_user_model()


def forgot_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = request.build_absolute_uri(f"/reset/{uid}/{token}/")

                send_mail(
                    subject='Password Reset Request',
                    message=f'Click the link below to reset your password:\n{reset_url}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                messages.success(request, 'Password reset link sent to your email.')
                return redirect('password_reset_done')
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email.')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'forgot_password.html', {'form': form})


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset successfully!')
                return redirect('login')
        else:
            form = CustomSetPasswordForm(user)
        return render(request, 'reset_password.html', {'form': form})
    else:
        messages.error(request, 'Invalid or expired reset link.')
        return redirect('password_reset')
    