# Command to run : python manage.py shell  < scripts/seed.py
from django.conf import settings
from django.contrib.auth.models import User
from event.models import Event, SubEvent, Addon
from base.utils import get_file_content
from django.core.files.base import ContentFile

def check_database():
    if len(User.objects.all()) > 0:
        print(
            "Are you sure you want to wipe the existing development database and reseed it? (Y/N)"
        )
        if settings.TEST or input().lower() == "y":
            destroy_database()
            return True
        else:
            return False
    else:
        return True


def destroy_database():
    print("Destroying existing database...")
    print("Destroying User objects...")
    User.objects.all().delete()
    return True


def create_user(is_admin, username=""):
    """
    Creates superuser, participant user, host user and returns it.
    """
    if settings.DEBUG:
        if is_admin:
            username = "admin"
            email = "admin@example.com"
            password = "password"
        else:
            email = "%s@example.com" % (username)
            password = "password"
    else:
        if is_admin:
            username = settings.ADMIN_USERNAME
            email = settings.ADMIN_EMAIL
            password = settings.ADMIN_PASSWORD

    user = User.objects.create_user(
        email=email,
        username=username,
        password=password,
        is_staff=is_admin,
        is_superuser=is_admin,
    )
    print(
        "{} was created with username: {} password: password".format(
            "Super user" if is_admin else "User", username
        )
    )
    return user

def create_event():
    event = Event.objects.create(
        name="Sabrang",
        description="Sabrang is the flagship annual festival of J K Lakshmipat University, Jaipur (JKLU). Since 2011, Sabrang has been celebrated annually, with the objective to provide students from different colleges and universities an opportunity to display their talents.",
        start_date="2023-09-26",
        end_date="2023-09-29",
        image= ContentFile(get_file_content("example/logo/sabrang-cover-text-e1664621537950.jpg", "rb"), "logo.jpg"),
        location="JKLU, Jaipur",
        price=300.00,
        sub_events_included_allowed=3,
        is_active=True,
        event_page="",
        payment_gateway="razorpay",
    )
    print("Sabrang was created")
    return event

def create_sub_event(event):
    SubEvent.objects.create(
        name="Panache",
        description="This is a sub event of Sabrang",
        start_date="2023-09-26",
        end_date="2020-09-29",
        image= ContentFile(get_file_content("example/logo/3-725x1024.jpg", "rb"), "logo1.jpg"),
        price=100.00,
        event=event,
        is_active=True,
    )
    SubEvent.objects.create(
        name="Step Up",
        description="This is a sub event of Sabrang",
        start_date="2023-09-26",
        end_date="2020-09-29",
        image= ContentFile(get_file_content("example/logo/4-725x1024.jpg", "rb"), "logo2.jpg"),
        price=100.00,
        event=event,
        is_active=True,
    )
    SubEvent.objects.create(
        name="Band Jam",
        description="This is a sub event of Sabrang",
        start_date="2023-09-26",
        end_date="2020-09-29",
        image= ContentFile(get_file_content("example/logo/1-725x1024.jpg", "rb"), "logo3.jpg"),
        price=100.00,
        event=event,
        is_active=True,
    )
    SubEvent.objects.create(
        name="Court Room",
        description="This is a sub event of Sabrang",
        start_date="2023-09-26",
        end_date="2020-09-29",
        image= ContentFile(get_file_content("example/logo/6-725x1024.jpg", "rb"), "logo4.jpg"),
        price=100.00,
        event=event,
        is_active=True,
    )
    SubEvent.objects.create(
        name="Bland Coding",
        description="This is a sub event of Sabrang",
        start_date="2023-09-26",
        end_date="2020-09-29",
        image= ContentFile(get_file_content("example/logo/5-725x1024.jpg", "rb"), "logo5.jpg"),
        price=100.00,
        event=event,
        is_active=True,
    )
    SubEvent.objects.create(
        name="Bidding",
        description="This is a sub event of Sabrang",
        start_date="2023-09-26",
        end_date="2020-09-29",
        image= ContentFile(get_file_content("example/logo/2-725x1024.jpg", "rb"), "logo6.jpg"),
        price=100.00,
        event=event,
        is_active=True,
    )
    SubEvent.objects.create(
        name="Marketing Mystros",
        description="This is a sub event of Sabrang",
        start_date="2023-09-26",
        end_date="2020-09-29",
        image= ContentFile(get_file_content("example/logo/7-768x1085.jpg", "rb"), "logo7.jpg"),
        price=100.00,
        event=event,
        is_active=True,
    )
    print("Sub Events was created")

def create_addon(event):
    Addon.objects.create(
        name="Hostel",
        icon="hotel",
        price=300.00,
        event=event,
        stock=10,
        is_active=True,
    )
    print("Addon 1 was created")


def run(*args):
    try:
        status = check_database()
        if status is False:
            print("Seeding aborted.")
            return 0
        print("Seeding...")
        # Create superuser
        create_user(is_admin=True)
        event = create_event()
        create_sub_event(event)
        create_addon(event)
        print("Database successfully seeded.")
    except Exception as e:
        print(e)