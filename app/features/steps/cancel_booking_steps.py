from behave import given, when, then

# فرض کنید که یک کلاس برای رزروهای شما وجود دارد.
class BookingSystem:
    def __init__(self):
        self.bookings = {}
        self.seats_available = 100  # فرض کنید که 100 صندلی موجود است

    def make_booking(self, user_id, event):
        if self.seats_available > 0:
            self.bookings[user_id] = event
            self.seats_available -= 1
            return True
        return False

    def cancel_booking(self, user_id):
        if user_id in self.bookings:
            event = self.bookings.pop(user_id)
            self.seats_available += 1
            return True
        return False


# ایجاد یک شی از سیستم رزرو
booking_system = BookingSystem()

@given('I have made a booking for a specific event')
def step_impl(context):
    # فرض کنید که شما یک رزرو برای رویداد "Concert" انجام داده‌اید
    context.user_id = "user123"
    context.event = "Concert"
    booking_system.make_booking(context.user_id, context.event)

@given('my plans have changed')
def step_impl(context):
    # فرض می‌کنیم که برنامه‌های کاربر تغییر کرده است
    context.plans_changed = True

@when('I attempt to cancel the booking')
def step_impl(context):
    # لغو رزرو
    context.result = booking_system.cancel_booking(context.user_id)

@then('the booking should be cancelled and the seats should be freed up')
def step_impl(context):
    # بررسی که رزرو لغو شده و صندلی‌ها آزاد شده‌اند
    assert context.result is True
    assert booking_system.seats_available == 100  # صندلی‌ها باید به حالت اولیه برگشته باشند
    assert context.user_id not in booking_system.bookings  # رزرو باید لغو شده باشد
