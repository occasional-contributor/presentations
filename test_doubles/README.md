class: center, middle

# Understanding Test Doubles
## Principles and Python Implementations

???

Welcome everyone. Today, we'll be discussing Test Doubles, a crucial concept in software testing, focusing on their categorization as popularized by Robert C. Martin, and how we can implement them in Python.

The goal is to equip you with the knowledge to write more robust, isolated, and maintainable tests.

---

## The Rationale for Test Doubles

Consider a common scenario in software development: testing a unit of code that has dependencies. These dependencies might include:

*   External APIs: Potentially slow, unreliable, or incurring costs per call.
*   Databases: Requiring setup, prone to state-related issues, and can slow down test execution.
*   Complex internal components: Difficult to instantiate or manage for a specific test case.

--

Such dependencies can introduce several challenges to unit testing:
*   **Reduced Speed**: Test suites become slow due to I/O operations or network latency.
*   **Increased Fragility**: Tests may fail due to external factors unrelated to the code under test.
*   **Obscured Isolation**: It becomes difficult to determine if a test failure originates from the unit itself or its dependency.
*   **Complex Setup**: Configuring dependencies to a specific state for each test can be cumbersome.

--

Test Doubles address these challenges by replacing real dependencies with controlled substitutes during testing.

.footnote[The categorization of Test Doubles discussed here is largely based on the work of Gerard Meszaros and popularized by Robert C. Martin.]

???

Before we dive into the types of test doubles, it's important to understand *why* we need them.

Real-world systems are complex. Our units of code rarely live in complete isolation.

When these dependencies are problematic for testing – due to speed, reliability, or setup complexity – test doubles become invaluable.

They allow us to focus our tests squarely on the logic of the unit we are interested in, leading to more effective and efficient testing cycles.

---

## The "System Under Test" (SUT)

A foundational concept in this discussion is the **System Under Test** (SUT).

*   **SUT**: This refers to the specific module, class, method, or function that is the target of a particular test.

Test doubles are typically employed to replace the **collaborators** or **dependencies** of the SUT, enabling focused testing of the SUT's logic in isolation.

```python
# Illustrative SUT:
def process_financial_transaction(transaction_data, payment_processor, audit_logger):
    # SUT logic:
    # payment_processor and audit_logger are collaborators.
    if payment_processor.execute_charge(transaction_data['amount']):
        audit_logger.log_success(transaction_data['id'])
        return "Transaction successful."
    else:
        audit_logger.log_failure(transaction_data['id'], payment_processor.get_last_error())
        return "Transaction failed."

# During testing, payment_processor and audit_logger would be
# replaced with appropriate test doubles.
```

The primary objective is to test `process_financial_transaction` independently of the actual `payment_processor` and `audit_logger` implementations.

???

It's crucial to clearly define what your System Under Test, or SUT, is for any given test.
This clarity helps in identifying which dependencies need to be replaced by doubles.
In our example, `process_financial_transaction` is the SUT. We want to verify its logic – how it interacts with the payment processor and logger under different conditions – without actually hitting a real payment gateway or writing to a persistent log during the test.

---

## Categorization of Test Doubles

There are five commonly recognized categories of test doubles:

1.  **Dummy** Objects
2.  **Fake** Objects
3.  **Stub** Objects
4.  **Spy** Objects
5.  **Mock** Objects

We will explore each category with Python examples, primarily utilizing the `unittest.mock` library.

???

These categories provide a useful vocabulary for discussing and designing tests.

Each type serves a distinct purpose in how it substitutes for a real dependency and what aspects of the SUT's interaction it helps verify.

Understanding these distinctions is key to choosing the right type of double for your testing needs.

---

## 1. Dummy Objects

### Purpose
Dummies are passed as arguments to satisfy parameter requirements but are never actually used by the SUT in the specific code path being tested.

### Behavior
They generally have no functional behavior. If their methods are invoked unexpectedly, they might do nothing or raise an error.

### Verification
Typically, no assertions are made against a Dummy object. Its presence is solely to allow the SUT to execute.

---

### Python Example: Dummy

Consider a `ReportGenerator` requiring a `Configuration` object, but for a test focusing on formatting, specific configuration values are irrelevant.

.columns[
.column[
```python
class ReportData:
    def __init__(self, title, content):
        self.title = title
        self.content = content

class ReportGenerator:
    def __init__(self, config_settings): # config_settings is a dependency
        self.config_settings = config_settings # May use for other methods

    def format_basic_report(self, data: ReportData):
        # This specific method might not use self.config_settings
        header = f"Report Title: {data.title}\n"
        body = f"Content:\n{data.content}"
        return header + body
```
]
.column[
```py
import unittest
from unittest.mock import Mock

class TestReportGenerator(unittest.TestCase):
    def test_basic_report_formatting(self):
        # dummy_config can be a simple object() if no methods are called.
        # Using Mock is safer if there's a chance an attribute might be accessed.
        dummy_config = Mock()

        generator = ReportGenerator(config_settings=dummy_config)
        report_content = ReportData("Sales Q1", "Total sales: $100,000")

        formatted_report = generator.format_basic_report(report_content)

        self.assertIn("Report Title: Sales Q1", formatted_report)
        self.assertIn("Total sales: $100,000", formatted_report)
        # No assertions are made about dummy_config.
```
]
]

In this case, `dummy_config` fulfills the `ReportGenerator`'s constructor requirement. If `format_basic_report` does not interact with `config_settings`, a simple `object()` or a `Mock` instance suffices.

???

Dummies are the simplest form of test doubles.

Their primary role is to fill space. If the SUT requires an argument but doesn't use it in the specific scenario you're testing, a dummy is appropriate.

The key here is that the dummy object's methods or attributes are *not* expected to be invoked by the SUT during this particular test.

Using `unittest.mock.Mock` as a dummy is often a safe choice as it will accept any attribute access or method call without error by default, unless configured otherwise.

---

## 2. Fake Objects

### Purpose
Fakes provide a simplified, but functional, alternative implementation of a dependency. They are often used for complex dependencies like databases or external services.

### Behavior
Fakes have working methods that simulate the behavior of the real component, often using in-memory data structures instead of external resources.

### Verification
Assertions can be made against the state of the Fake object after the SUT has interacted with it.

---

### Python Example: Fake

A `CustomerService` that typically interacts with a database via a `CustomerRepository`.

.columns[
.column[
```python
class Customer:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class CustomerService:
    def __init__(self, customer_repo):
        self.customer_repo = customer_repo

    def create_customer(self, name, email):
        customer_id = self.customer_repo.generate_new_id()
        new_customer = Customer(customer_id, name, email)
        self.customer_repo.save(new_customer)
        return new_customer
```
]
.column[
```py
class FakeCustomerRepository:
    def __init__(self):
        self._customers = {} # In-memory storage
        self._next_id = 1

    def generate_new_id(self):
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def save(self, customer: Customer):
        self._customers[customer.id] = customer

    def find_by_id(self, customer_id: int):
        return self._customers.get(customer_id)
```
]
]

---

```py
import unittest
class TestCustomerServiceWithFake(unittest.TestCase):
    def test_create_customer_persists_via_fake_repo(self):
        fake_repo = FakeCustomerRepository()
        customer_service = CustomerService(customer_repo=fake_repo)

        customer = customer_service.create_customer("John Doe", "john.doe@example.com")

        self.assertIsNotNone(customer)
        self.assertEqual(customer.name, "John Doe")
        # Verify by inspecting the state of the Fake repository
        retrieved_customer = fake_repo.find_by_id(customer.id)
        self.assertIsNotNone(retrieved_customer)
        self.assertEqual(retrieved_customer.name, "John Doe")
```

The `FakeCustomerRepository` uses a dictionary for storage, avoiding database interactions, making tests faster and more predictable.

???

Fakes are more sophisticated than Dummies. They provide a working, albeit simplified, implementation of the dependency.

This is particularly useful for things like repositories or services where the SUT needs to interact with the dependency and observe state changes.

The `FakeCustomerRepository` here simulates database operations using a Python dictionary. This allows us to test the `CustomerService`'s logic of creating and saving a customer without the overhead and complexity of a real database.

Verification often involves checking the internal state of the fake object after the SUT has acted.

---

## 3. Stubs

### Purpose
Stubs provide pre-programmed responses to method calls made by the SUT. They are used to control the data flow into the SUT from its dependencies.

### Behavior
When a method on a stub is invoked, it returns a specific, hardcoded value or raises a predefined exception, as configured for the test.

### Verification
Assertions are typically made on the SUT's state or return value, which is influenced by the data provided by the stub. The stub itself is usually not verified.

---

### Python Example: Stub

A `PricingService` that relies on an `ExchangeRateProvider` to get current rates.

.columns[
.column[
```python
from unittest.mock import Mock
import unittest

class PricingService:
    def __init__(self, exchange_rate_provider):
        self.exchange_rate_provider = exchange_rate_provider

    def calculate_price_in_usd(self, product_id: str, price_in_eur: float):
        rate = self.exchange_rate_provider.get_eur_to_usd_rate(product_id)
        if rate is None:
            return None # Or handle error
        return price_in_eur * rate
```
]
.column[
```py
class TestPricingService(unittest.TestCase):
    def test_calculates_usd_price_correctly_with_stubbed_rate(self):
        # Create a stub for ExchangeRateProvider
        stub_rate_provider = Mock()
        # Program the stub's method to return a specific value
        stub_rate_provider.get_eur_to_usd_rate.return_value = 1.10

        service = PricingService(exchange_rate_provider=stub_rate_provider)
        usd_price = service.calculate_price_in_usd("product123", 100.0)

        self.assertAlmostEqual(usd_price, 110.0)
        # Optionally, verify the stub was called as expected
        # (though this leans towards Spy behavior)
        stub_rate_provider.get_eur_to_usd_rate.assert_called_once_with(
            "product123"
        )
```
]
]

Here, `stub_rate_provider.get_eur_to_usd_rate` is configured to return `1.10`, allowing isolated testing of the `PricingService`'s calculation logic.

???

Stubs are all about providing controlled input to your SUT.

When your SUT calls a method on a dependency, a stub will return a predefined value. This allows you to test different code paths within your SUT by varying the data returned by its stubs.

In this example, we're not concerned with how the `ExchangeRateProvider` actually gets the rate; we just provide a fixed rate (1.10) to test the `PricingService`'s multiplication logic.

The primary verification is on the SUT's output (the `usd_price`), not the stub itself, although `unittest.mock` makes it easy to also check if the stub was called as expected.

---

## 4. Spies

### Purpose
Spies are stubs that also record information about how they were called by the SUT (e.g., methods invoked, arguments passed, number of invocations).

### Behavior
They return canned data like stubs, but additionally capture details of their interactions with the SUT.

### Verification
Assertions are made to verify that the SUT interacted with the spy correctly. This is often termed *behavior verification*.

---

### Python Example: Spy

An `AuditService` that logs actions. We want to verify that a specific logging method is called.

.columns[
.column[
```python
from unittest.mock import Mock
import unittest

class UserActionService:
    def __init__(self, audit_logger):
        self.audit_logger = audit_logger # Dependency to be spied upon

    def perform_critical_action(self, user_id: str, action_details: str):
        # ... critical action logic ...
        self.audit_logger.log_action(
            user_id=user_id,
            action_type="CRITICAL_ACTION",
            details=action_details
        )
        return True
```
]
.column[
```py
class TestUserActionService(unittest.TestCase):
    def test_critical_action_is_logged(self):
        spy_audit_logger = Mock() # This Mock will act as a spy

        service = UserActionService(audit_logger=spy_audit_logger)
        service.perform_critical_action(
            user_id="user_abc",
            action_details="Data update",
        )

        # Verify the spy was called as expected
        spy_audit_logger.log_action.assert_called_once_with(
            user_id="user_abc",
            action_type="CRITICAL_ACTION",
            details="Data update"
        )
```
]
]

The `spy_audit_logger` allows verification that `log_action` was invoked by the SUT with the correct parameters, without needing to inspect actual log outputs.

???

Spies take stubs a step further. While they can provide canned responses like stubs, their main purpose is to record how the SUT interacts with them.

You use a spy when you need to verify that the SUT made certain calls to its dependency, perhaps with specific arguments, or a certain number of times. This is known as behavior verification.

Here, we're not checking the return value of `perform_critical_action` as much as we are ensuring it correctly calls the `audit_logger`. The `Mock` object from `unittest.mock` is excellent for this, as it automatically records call information.

---

## 5. Mocks (Strict Definition)

### Purpose
Mocks are objects pre-programmed with expectations regarding the calls they should receive from the SUT. They verify these interactions during or after the test.

### Behavior
Mocks define an expected sequence and nature of calls. A test will typically fail if these expectations are not met (e.g., unexpected method called, expected method not called, wrong arguments).

### Verification
The mock object itself often performs the verification. The test sets up expectations, executes the SUT, and then typically asks the mock to verify that all expectations were satisfied.

---

### Python Example: Mock

An `OrderFulfillmentService` that interacts with `InventoryManager` and `ShipmentScheduler`.

```python
class OrderFulfillmentService:
    def __init__(self, inventory_mgr, shipment_sched):
        self.inventory_mgr = inventory_mgr
        self.shipment_sched = shipment_sched

    def fulfill_order(self, order_id: str, items: list, shipping_address: str):
        if not self.inventory_mgr.check_stock_and_reserve(order_id, items):
            self.inventory_mgr.log_stock_issue(order_id, "Insufficient stock")
            return False

        tracking_number = self.shipment_sched.schedule_shipment(order_id, items, shipping_address)
        if tracking_number:
            self.inventory_mgr.confirm_shipment(order_id, tracking_number)
            return True
        else:
            self.inventory_mgr.release_stock(order_id) # Rollback
            return False
```

---

.columns[
.column[
```py
from unittest.mock import Mock, call
import unittest

class TestOrderFulfillmentService(unittest.TestCase):
    def test_successful_order_fulfillment_invokes_dependencies_correctly(self):
        mock_inventory_mgr = Mock()
        mock_shipment_sched = Mock()

        # Configure stubbed return values for the success path
        mock_inventory_mgr.check_stock_and_reserve.return_value = True
        mock_shipment_sched.schedule_shipment.return_value = "TRACKING123"

        service = OrderFulfillmentService(
            inventory_mgr=mock_inventory_mgr,
            shipment_sched=mock_shipment_sched
        )
        order_details = {
            "id": "order001",
            "items": ["itemA", "itemB"],
            "address": "123 Main St"
        }
        result = service.fulfill_order(
            order_details["id"],
            order_details["items"],
            order_details["address"],
        )
```
]
.column[
```py
        self.assertTrue(result)

        # Verify interactions (Mock verification)
        expected_inventory_calls = [
            call.check_stock_and_reserve("order001", ["itemA", "itemB"]),
            call.confirm_shipment("order001", "TRACKING123")
        ]
        mock_inventory_mgr.assert_has_calls(
            expected_inventory_calls, any_order=False
        )
        # Or more specific assertions:
        # mock_inventory_mgr.check_stock_and_reserve.assert_called_once_with(
        #     "order001", ["itemA", "itemB"]
        # )
        # mock_inventory_mgr.confirm_shipment.assert_called_once_with(
        #     "order001", "TRACKING123"
        # )

        mock_shipment_sched.schedule_shipment.assert_called_once_with(
            "order001", ["itemA", "itemB"], "123 Main St"
        )
```
]
]

Python's `unittest.mock.Mock` facilitates this by recording calls, which are then asserted post-interaction. Some frameworks allow setting expectations upfront that cause immediate failure on deviation.

???

Mocks are often considered the strictest type of test double. They are concerned with the precise sequence and details of interactions between the SUT and its collaborators.

You define expectations on the mock object – which methods should be called, in what order, and with what arguments. The test fails if these expectations aren't met.

In Python's `unittest.mock`, this is typically done by asserting call history after the SUT has run. The `assert_called_once_with`, `assert_any_call`, and `assert_has_calls` methods are key here.

While powerful for verifying complex interactions, overusing mocks can lead to brittle tests that are too tightly coupled to the SUT's implementation details.

---

## Summary of Test Double Categories

| Double Type | Primary Purpose                              | Behavior Characteristics                  | Verification Focus                                  |
| ----------- | -------------------------------------------- | ----------------------------------------- | --------------------------------------------------- |
| **Dummy**   | Satisfy parameter lists                      | Minimal or no functionality               | Generally none; SUT executes without error          |
| **Fake**    | Provide a simplified, working implementation | Simulates real behavior (e.g., in-memory) | State of the Fake after SUT interaction             |
| **Stub**    | Supply controlled data to the SUT            | Returns pre-programmed responses          | SUT's state or return value (state verification)    |
| **Spy**     | Stub functionality + record interactions     | Returns responses, captures call details  | How the SUT invoked the Spy (behavior verification) |
| **Mock**    | Verify SUT interactions against expectations | Pre-defined expectations for calls        | Interactions strictly match expectations (behavior) |

--

## Significance of these distinctions
### Clarity of Intent
Aids in precisely defining the test's objective.

### Improved Communication
Provides a shared lexicon for development teams.

### Enhanced Test Design
Guides the selection of appropriate doubles for specific testing goals, distinguishing between state and behavior verification.

???

This table provides a concise summary of the five types of test doubles.

Understanding these distinctions is crucial for effective test design. It helps you choose the right tool for the job.

Are you trying to feed specific data into your SUT? A stub might be best.

Do you need to ensure your SUT calls another service correctly? A spy or mock would be appropriate.

Is the dependency complex but its simplified behavior is sufficient for the test? A fake can be very useful.

This shared vocabulary also improves team communication about testing strategies.

---

## `unittest.mock`: A Versatile Tool in Python

Python's standard `unittest.mock` module provides highly flexible objects, primarily `Mock` and `MagicMock`, that can fulfill the roles of Dummies, Stubs, Spies, and Mocks.

```python
from unittest.mock import Mock, MagicMock, patch, call

# General purpose Mock object
generic_mock = Mock()

# Configuring as a Stub:
generic_mock.get_data.return_value = {"status": "success", "value": 123}
generic_mock.process_item.side_effect = Exception("Processing failed")

# Using as a Spy/Mock (post-interaction verification):
# (After SUT has called generic_mock.get_data('item_id_x'))
generic_mock.get_data.assert_called_once_with('item_id_x')

# Verifying call counts and arguments:
# generic_mock.some_method.call_count
# generic_mock.some_method.call_args
# generic_mock.some_method.call_args_list

# MagicMock for mocking Python's special (magic) methods:
magic_m = MagicMock()
magic_m.__str__.return_value = "Mocked String"
# str(magic_m) would return "Mocked String"
```

The specific role a `Mock` object plays is determined by how it's configured and what assertions are made against it in the test.

???

The `unittest.mock` library is the de facto standard for creating test doubles in Python.

Its `Mock` class is incredibly versatile. You don't necessarily create a `StubMock` or a `SpyMock`. Instead, you create a `Mock` object and then configure its `return_value`, `side_effect`, and later use its assertion methods (`assert_called_with`, `assert_has_calls`, etc.) to achieve the behavior of a stub, spy, or mock.

`MagicMock` is a subclass of `Mock` that comes with default implementations for most magic methods, which can be very convenient.

The key is to understand the *role* you need the double to play, and then use `unittest.mock`'s features to implement that role.

---

## Guidance on Selecting Test Doubles

### Dummy
* Use when a parameter is syntactically required but logically unused in the SUT's tested code path.

### Fake
* Ideal for dependencies where a simpler, stateful, in-memory version can effectively replace a heavier component (e.g., database, file system).
* Consider if the Fake's complexity warrants its own tests.

### Stub
* Best when the SUT's logic depends on specific data returned by a dependency.
* Stubs allow precise control over this data flow to test various execution paths.

### Spy
* Employ when verifying that the SUT performs a specific action (e.g., logs an event, sends a notification) that doesn't directly affect the SUT's primary return value or testable state.
* Focuses on "command" interactions.

### Mock
* Suited for scenarios where the exact sequence and nature of interactions with one or more dependencies are critical to the SUT's correctness (e.g., an orchestrator pattern). Exercise caution to avoid overly brittle tests tied to implementation minutiae.
* Over-reliance on Mocks for verifying every interaction can lead to tests that are tightly coupled to the SUT's internal implementation. Refactoring the SUT, even without changing its external contract, might then break numerous tests. A balance is essential.

???

Choosing the appropriate test double depends on the specific testing objective.

Choosing the right double is an art as much as a science, but here are some guidelines.

If you just need to fill a slot, use a Dummy.

If you need a lightweight, working version of something complex, use a Fake. Be mindful that Fakes themselves don't become overly complex.

If you need to control the data your SUT receives to test different paths, use a Stub. This is very common for state verification.

If you need to check that your SUT *told* another component to do something, use a Spy. This is for behavior verification of commands.

If the *entire protocol* of interaction is what you're testing, use a Mock. But be wary of creating tests that are too fragile.

The key question is always: "What am I trying to verify in *this specific test*?" Let that guide your choice.

It's often a trade-off between verification thoroughness and test maintainability.

---

## Key Principles and Benefits

### Isolation
Test Doubles are fundamental for isolating the System Under Test, ensuring tests focus on a single unit of logic.

### Determinism & Speed
They contribute to faster and more reliable tests by eliminating external uncertainties and I/O overhead.

### Testability
They enable testing of code that would otherwise be difficult or impossible to test effectively in isolation.

### Conceptual Framework
The categorization (Dummy, Fake, Stub, Spy, Mock) offers a valuable vocabulary and mental model for designing and discussing tests.

### Strategic Focus
Differentiate between testing an SUT's **state** (outcome-based, often with Stubs/Fakes) versus its **behavior** (interaction-based, often with Spies/Mocks).

???

To summarize, test doubles are a powerful technique for achieving effective unit testing.

They help us write tests that are focused, fast, reliable, and maintainable.

By understanding the different types of doubles, we can make more informed decisions about our testing strategies.

Remember to focus on what you're testing: is it the final state or return value of your SUT, or is it the way your SUT interacts with its collaborators? This distinction will often point you to the right kind of double.

And finally, always aim for clarity and simplicity in your tests. The test double should make the test *easier* to understand, not harder.

---

## Considerations for Effective Use

*   Focus tests on verifying one aspect of the SUT at a time.
*   Favor testing the SUT's public API and observable behavior over its internal implementation details.
*   Strive for a balance. Use the simplest double that achieves the testing goal.

???

And finally, always aim for clarity and simplicity in your tests. The test double should make the test *easier* to understand, not harder.

---
class: center, middle

# Questions and Discussion

???

Thank you for your attention. I'm now open to any questions or further discussion on test doubles and their application.

.footnote[Presentation based on concepts by Gerard Meszaros and Robert C. Martin]
