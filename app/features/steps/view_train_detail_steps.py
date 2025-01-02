from behave import given, when, then

# فرض می‌کنیم که داده‌های قطار در اینجا قرار دارند
train_data = {
    "train_1": {
        "departure_time": "8:00 AM",
        "arrival_time": "10:00 AM",
        "class_type": "Economy"
    },
    "train_2": {
        "departure_time": "10:00 AM",
        "arrival_time": "12:00 PM",
        "class_type": "Business"
    }
}

# سناریو 1: ورود به سیستم و انتخاب قطار معتبر
@given('the user is logged in to the system')
def step_given_user_logged_in(context):
    context.logged_in = True  # فرض می‌کنیم کاربر وارد شده است

@given('the user selects a train')
def step_given_user_selects_train(context):
    context.selected_train = "train_1"  # فرض می‌کنیم که کاربر قطار معتبری را انتخاب کرده است

@when('the user views the train details')
def step_when_user_views_train_details(context):
    # در اینجا جزئیات قطار انتخابی را برمی‌گردانیم
    selected_train = context.selected_train
    context.train_details = train_data.get(selected_train, None)

@then('the user sees the departure time, arrival time, and class type of the train')
def step_then_user_sees_train_details(context):
    assert context.train_details is not None, "Train details not found"
    assert "departure_time" in context.train_details
    assert "arrival_time" in context.train_details
    assert "class_type" in context.train_details
    print("Train Details:", context.train_details)

# سناریو 2: انتخاب قطار غیرموجود
@given('the user selects a non-existent train')
def step_given_user_selects_non_existent_train(context):
    context.selected_train = "non_existent_train"  # فرض می‌کنیم که کاربر قطار غیرموجود را انتخاب کرده است

@then('the system displays an error message indicating that the train does not exist')
def step_then_system_displays_error_message(context):
    assert context.train_details is None, "Train details should be None for a non-existent train"
    print("Error: The selected train does not exist.")

# سناریو 3: عدم انتخاب قطار
@given('the user has not selected a train')
def step_given_user_has_not_selected_train(context):
    context.selected_train = None  # فرض می‌کنیم که کاربر قطاری انتخاب نکرده است

@then('the system displays a message indicating that no train is selected')
def step_then_system_displays_no_train_selected_message(context):
    assert context.selected_train is None, "No train should be selected"
    print("Message: No train selected.")
