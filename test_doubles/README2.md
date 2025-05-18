class: center, middle

# Uncle Bob's Test Doubles
## 🕵️‍♂️ Keeping Your Python Tests Clean & Focused 🐍

---

## Why Bother with Test Doubles? 🤔

Picture this: you're testing a small, neat function. But...

*   It calls an **external API** (slow, might be down, costs money!).
*   It talks to a **database** (needs setup, slow, stateful).
*   It uses another **complex class** that's hard to instantiate or has its own bugs.

These dependencies can make your tests:
*   **Slow**: Waiting for networks or databases.
*   **Brittle/Flaky**: External factors cause failures, not your code.
*   **Hard to Isolate**: Is the bug in *your* code or the dependency?
*   **Difficult to Set Up**: Getting a database into a specific state for a test can be a pain.

**Test Doubles to the rescue!** They stand in for real dependencies, giving you control.

.footnote[Uncle Bob (Robert C. Martin) didn't invent all these terms, but he popularized and clearly defined them!]

---

## The "System Under Test" (SUT) 🧪

This is a key term!

*   **SUT**: The specific piece of code (function, method, class) that you are currently trying to test.

When we use a test double, it's usually to replace a **collaborator** or **dependency** of the SUT.

```py
# Example: Our SUT might be this function
def process_order(
    order_data,
    payment_gateway,
    inventory_system,
):
    # SUT logic here
    # payment_gateway and inventory_system are collaborators
    if payment_gateway.charge(order_data['amount']):
        inventory_system.decrement(order_data['item_id'])
        return "Order processed!"
    return "Payment failed."

# In a test, we'd replace payment_gateway and inventory_system with doubles.
```

Our goal is to test `process_order` in *isolation*.

---

## The Lineup: Uncle Bob's 5 Test Doubles 🫆

1.  **Dummy** Objects
2.  **Fake** Objects
3.  **Stub** Objects
4.  **Spy** Objects
5.  **Mock** Objects

Let's meet them one by one! We'll use Python's `unittest.mock` library (often aliased as `mock`) for many examples, as it's super versatile.

---

## Dummy Objects 🧸

*   **Purpose**: Passed around but *never actually used*. They are just there to fill parameter lists.
*   **Behavior**: They don't do anything. Their methods, if called, might raise an error or do nothing.
*   **Verification**: You don't usually verify anything about a Dummy.

---

## .dimmed[Dummy Objects 🧸] Python Example

Imagine a `NotificationService` that needs a `Logger` instance, but for a particular test, we don't care about logging.

.columns[
.column[
```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class NotificationService:
    def __init__(self, logger):  # logger is a dependency
        self.logger = logger

    def notify_user_registered(self, user: User):
        message = f"User {user.name} registered with email {user.email}."
        # In a real scenario, this might send an email, SMS, etc.
        print(f"Pretending to send notification: {message}")
        self.logger.info(f"Notification sent for user {user.name}")
        # We want to ignore this
```
]
.column[
```py
class TestNotificationService(unittest.TestCase):
    def test_user_registration_notification_flow(self):
        dummy_logger = object()  # Simplest possible dummy
        # Or:
        # from unittest.mock import Mock
        # dummy_logger = Mock()

        service = NotificationService(logger=dummy_logger)
        alice = User("Alice", "alice@example.com")

        # We're just checking the service doesn't crash and
        # perhaps that some side effect *we control* happens.
        # For this example, we're not asserting much.
        service.notify_user_registered(alice)
        # No assertions on dummy_logger needed.
```
]
]

Here, `dummy_logger` just needs to exist.

If `notify_user_registered` *didn't* actually call `self.logger.info()`, `object()` would be fine. If it *did* call it, `object()` would raise an `AttributeError`.

A `unittest.mock.Mock()` would happily accept any call without error, making it a slightly more robust dummy.

---

## Fake Objects 🎭

*   **Purpose**: Provide a simpler, working implementation of a dependency. Good for things like in-memory databases or simple versions of complex services.
*   **Behavior**: They actually *work*, but in a simplified way (e.g., an in-memory list instead of a real database).
*   **Verification**: You might inspect the state of the Fake after the test.

---

## .dimmed[Fake Objects 🎭] Python Example

.columns[
.column[
Let's fake a `UserRepository` that usually talks to a database.

The `FakeUserRepository` mimics the real one but uses a simple dictionary.

It's way faster and totally predictable.
]
.column[
```py
# The real UserRepository might look like this (conceptual)
# class RealUserRepository:
#     def save(self, user: User): # Connects to DB, SQL INSERT, etc. ...
#     def get_by_id(self, user_id: int): # SQL SELECT ...

class FakeUserRepository:  # The Fake implementation
    def __init__(self):
        self._users = {}  # In-memory storage
        self._next_id = 1

    def get_next_id(self):
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def save(self, user: User):
        print(f"FakeRepo: Saving user {user.name}")
        self._users[user.id] = user # Assumes user has an 'id' attribute

    def get_by_id(self, user_id: int):
        return self._users.get(user_id)
```
]
]

---

## .dimmed[Fake Objects 🎭 Python Example]

.columns[
.column[
```py
class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def register_user(self, name, email):
        user_id = self.user_repo.get_next_id()
        new_user = User(user_id, name, email)
        self.user_repo.save(new_user)
        return new_user
```
]
.column[
```py
class TestUserServiceWithFake(unittest.TestCase):
    def test_register_user_saves_to_fake_repo(self):
        fake_repo = FakeUserRepository()
        user_service = UserService(user_repo=fake_repo)

        user = user_service.register_user("Bob", "bob@example.com")

        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Bob")
        # Verify by checking the state of the Fake
        retrieved_user = fake_repo.get_by_id(user.id)
        self.assertEqual(retrieved_user.name, "Bob")
```
]
]

---

## Stubs 📜

*   **Purpose**: Provide canned answers to calls made during the test. They "stub out" methods to return specific values needed for the SUT to proceed.
*   **Behavior**: When a method is called on a stub, it returns a pre-programmed response. It doesn't usually do much else.
*   **Verification**: You don't typically verify stubs themselves; you verify the SUT behaves correctly *because of* the data the stub provided.

---

## .dimmed[Stubs 📜] Python Example

.columns[
.column[
Imagine a `WeatherForecaster` that uses an external `WeatherService`.

We want to stub `WeatherService` to control the temperature it reports.
]
.column[
```py
class WeatherForecaster:
    def __init__(self, weather_service):
        self.weather_service = weather_service

    def get_clothing_recommendation(self, city: str):
        temp = self.weather_service.get_temperature(city)

        if temp < 0:
            return "Heavy coat, hat, and gloves!"

        if temp < 15:
            return "A warm jacket."

        return "Light clothing."
```
]
]

---

## .dimmed[Stubs 📜 Python Example]

.columns[
.column[
Here, `stub_weather_service.get_temperature` is programmed to always return `-5`.

This lets us test the "freezing temps" logic of our `WeatherForecaster` without a real API call.
]
.column[
```py
class TestWeatherForecaster(unittest.TestCase):
    def test_recommends_heavy_coat_for_freezing_temps(self):
        stub_weather_service = Mock()  # Create a stub for WeatherService
        stub_weather_service.get_temperature.return_value = -5  # Canned response

        forecaster = WeatherForecaster(weather_service=stub_weather_service)
        recommendation = forecaster.get_clothing_recommendation("Oslo")

        self.assertEqual(recommendation, "Heavy coat, hat, and gloves!")
        # We might also check that get_temperature was called, if important.
        stub_weather_service.get_temperature.assert_called_once_with("Oslo")
```
]
]

---

## Spies 👀

*   **Purpose**: A spy is a stub that also records some information about how it was called (e.g., which methods, how many times, with what arguments).
*   **Behavior**: It returns canned data (like a stub) but also "spies" on the calls.
*   **Verification**: You verify that the SUT called the spy correctly. This is often called *behavior verification*.

---

## .dimmed[Spies 👀] Python Example

Let's say we have a `DiscountService` that should log an event when a discount is applied. We'll use a spy for the logger.

The `spy_event_logger` records the call to `log_event`, and we can assert that it happened with the correct arguments.

This is super useful for verifying interactions where the SUT doesn't return a value directly related to the interaction.

.columns[
.column[
```python
class DiscountService:
    def __init__(self, event_logger):
        self.event_logger = event_logger # Dependency we'll spy on

    def apply_discount(self, user_id: int, discount_percentage: float):
        if discount_percentage > 0.5:  # Hypothetical logic
            self.event_logger.log_event(
                "LargeDiscountApplied",
                {"user_id": user_id, "discount": discount_percentage}
            )
            return "Discount too large, requires approval."

        self.event_logger.log_event(  # ... apply discount logic ...
            "DiscountApplied",
            {"user_id": user_id, "discount": discount_percentage}
        )

        return f"Applied {discount_percentage*100}% discount for user {user_id}."
```
]
.column[
```py
class TestDiscountService(unittest.TestCase):
    def test_logs_event_when_discount_applied(self):
        spy_event_logger = Mock()  # Mock can also act as a Spy

        service = DiscountService(event_logger=spy_event_logger)
        service.apply_discount(user_id=123, discount_percentage=0.1)

        # Verify the spy was called as expected
        spy_event_logger.log_event.assert_called_once_with(
            "DiscountApplied",
            {"user_id": 123, "discount": 0.1}
        )
```
]
]

---

## Mocks 🤖

*   **Purpose**: Mocks are pre-programmed with *expectations* of the calls they should receive. They will cause the test to fail if they aren't called exactly as expected.
*   **Behavior**: They know how they are supposed to be called. If they receive an unexpected call, or don't receive an expected one, they can raise an error.
*   **Verification**: The mock object itself often performs the verification. You set up expectations, run the SUT, and then ask the mock to verify itself.

---

## .dimmed[Mocks 🤖] Python Example

.columns[
.column[
Python's `unittest.mock.Mock` is very flexible. It can be used for stubs and spies easily. To use it as a "classic" mock, you often set up expectations on method calls *after* the SUT has interacted with it, then assert those expectations.

Some testing frameworks allow setting expectations *beforehand*, failing immediately on an unexpected call. `unittest.mock` is more about post-interaction verification.
]
.column[
```python
class OrderProcessor:
    def __init__(self, payment_gw, shipping_svc):
        self.payment_gw = payment_gw
        self.shipping_svc = shipping_svc

    def process(self, order):
        # 1. Charge payment
        try:
            self.payment_gw.charge(order.customer_id, order.amount)
        except Exception as e:  # Log error, don't ship
            print(f"Payment failed: {e}")
            return False

        # 2. If payment successful, arrange shipping
        self.shipping_svc.schedule_delivery(order.address, order.items)
        return True

class Order: # Simple data class
    def __init__(self, customer_id, amount, address, items):
        self.customer_id = customer_id
        self.amount = amount
        self.address = address
        self.items = items
```
]
]

---

## .dimmed[Mocks 🤖 Python Example]

.columns[
.column[
In this example, `mock_payment_gw` and `mock_shipping_svc` are set up.

After `processor.process()` runs, we use `assert_called_once_with` to verify they were interacted with *exactly* as expected.

This is behavior verification, characteristic of Mocks.

If `payment_gw.charge` was supposed to be called twice, or with different arguments, the test would fail.
]
.column[
```py
class TestOrderProcessor(unittest.TestCase):
    def test_process_charges_and_ships_on_success(self):
        mock_payment_gw = Mock()
        mock_shipping_svc = Mock()

        # Configure mock_payment_gw to not raise an exception (act as a stub for success)
        # If charge() was expected to return a value, we'd set it:
        # mock_payment_gw.charge.return_value = "transaction_id_123"

        processor = OrderProcessor(payment_gw=mock_payment_gw, shipping_svc=mock_shipping_svc)
        sample_order = Order(
            customer_id="cust456",
            amount=100.00,
            address="123 Main St",
            items=["itemA", "itemB"],
        )

        result = processor.process(sample_order)
        self.assertTrue(result)

        # Verify interactions (the "mock" aspect)
        mock_payment_gw.charge.assert_called_once_with(sample_order.customer_id, sample_order.amount)
        mock_shipping_svc.schedule_delivery.assert_called_once_with(sample_order.address, sample_order.items)
```
]
]

---

## A Note on Mocks vs. Spies 📝 

The line can be blurry, especially with flexible tools like `unittest.mock`.

Generally:
*   **Spies**: You check *after the fact* what happened.
    *   More about observing.
*   **Mocks**: You often define *expectations upfront* (though `unittest.mock` leans to post-verification).
    *   More about specifying required behavior.

---

## Quick Recap 📝

| Double Type | Main Purpose                              | Behavior                                     | Verification Focus                            |
| ----------- | ----------------------------------------- | -------------------------------------------- | --------------------------------------------- |
| **Dummy**   | Fill parameter lists                      | Does nothing, methods might not even exist   | None (or just that SUT doesn't crash)         |
| **Fake**    | Simpler, working implementation           | Actually works, but simplified (e.g. in-mem) | State of the Fake after SUT interaction       |
| **Stub**    | Provide canned answers                    | Returns pre-programmed values                | SUT's state/return value (state verification) |
| **Spy**     | Stub + record calls                       | Returns canned values, records interactions  | How the SUT called the Spy (behavior)         |
| **Mock**    | Verify calls against pre-set expectations | Knows expected calls, can fail if not met    | Interactions match expectations (behavior)    |

**Why is this distinction useful?**
*   **Clarity**: Helps you think about *why* you're replacing a dependency and *what* you want to achieve with the double.
*   **Communication**: Provides a shared vocabulary for your team.
*   **Test Design**: Guides you to write more focused tests. Are you testing state or behavior?

---

## `unittest.mock` - Your Python Swiss Army Knife 🇨🇭

.columns[
.column[
Python's built-in `unittest.mock` module is incredibly powerful.

A single `Mock` object can often serve as a Dummy, Stub, Spy, or Mock, depending on how you configure it and what you assert.
]
.column[
```python
from unittest.mock import Mock, MagicMock, patch

# Create a basic mock
m = Mock()

# Stubbing a return value
m.some_method.return_value = 42

# Stubbing a side effect (e.g., raising an exception)
m.another_method.side_effect = ValueError("Oops!")
```
]
]

.columns[
.column[
The key is understanding the *role* you want the double to play in your specific test.
]
.column[
```py
# Spying: After SUT interacts with m...
m.some_method.assert_called_once_with('arg1', 'arg2')
# For example: m.some_method.assert_called_once_with(
#     "some_value", "other_value"
# )
print(m.some_method.call_args_list) # See all calls

# MagicMock: For mocking magic methods like __str__
mm = MagicMock()
mm.__len__.return_value = 5
len(mm) # returns 5
```
]
]

---

## When to Use Which? 🤔

*   **Dummy**: When a parameter is required by a signature but truly isn't used in the code path you're testing.
    *   Keep it simple!
*   **Fake**: Great for replacing "heavy" dependencies like databases or file systems with lightweight in-memory versions.
    *   Useful when the SUT needs to interact quite a bit with the dependency and see state changes.
    *   *Speculation:* Fakes can sometimes grow complex themselves. If your Fake starts needing its own tests, it might be a sign it's too complicated, or maybe the SUT is doing too much.
*   **Stub**: Perfect when your SUT needs specific data from a dependency to follow a certain logic path.
    *   You control the data, you control the path.
*   **Spy**: Use when you want to check that an action happened (a call was made, an event was logged) but that action doesn't directly influence the SUT's return value or main state change you're testing.
    *   Good for "fire and forget" calls.
*   **Mock**: Best when the *interaction itself* is the core behavior you're testing.
    *   For example, in an orchestrator class that calls several services in a specific order.
    *   *Speculation:* Overusing Mocks (especially strict ones that verify call order and exact arguments for everything) can lead to brittle tests. If you refactor the SUT's internal implementation (but not its observable behavior), your mock-heavy tests might break. It's a balance!

---

## Key Takeaways ✨

*   Test Doubles help **isolate** your System Under Test.
*   They make tests **faster**, more **reliable**, and **easier to write**.
*   Uncle Bob's categories (Dummy, Fake, Stub, Spy, Mock) provide a useful **vocabulary** and **mental model**.
*   Python's *`unittest.mock`* is a flexible tool for creating most of these doubles.
*   Choose the right double for the job: focus on what you're *actually trying to test*.


### Think about
*   Am I testing **state** (the result, the data)?
    *   Stubs and Fakes are often good.
*   Am I testing **behavior** (the interactions, the calls made)?
    *   Spies and Mocks shine here.

---
class: center, middle

# Questions? 🤔

Happy Testing!
