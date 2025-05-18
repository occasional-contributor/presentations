class: center, middle

# Various Approaches to<br />Code Deduplication in Python

---

## The problem

Imagine we have an email application for sending emails. The *`send`* method in this application takes a sender, recipient and a message as parameters, and calls the `send` method of the sender.

```py
class EmailApp:
    def send(
        self,
        message,
        sender,
        recipients,
    ):
        sender.send(message, recipients)
```

There are two kinds of senders:

1. *`Mailbox`* is an email account where a user can log in to read and send email.
2. *`MailingList`* is an email account that exists only to forward emails to mailboxes and other mailing lists.

---

## The trivial implementation

.columns[
.column[
```py
@enum.unique
class EmailAddressType(enum.IntEnum):
    MAILBOX = auto()
    MAILINGLIST = auto()

class EmailAddress:
    id: UUID
    type: EmailAddressType
    addr: str

    pwd_hash: str | None                # Only useful if type == EmailAddressType.MAILBOX
    recipients: tuple[str, ...] | None  # Only useful if type == EmailAddressType.MAILINGLIST

    def send(
        self,
        message: str,
        recipients: tuple[str, ...] | None = None,
    ):
        if self.type == EmailAddressType.MAILBOX:
            return send_message(message, recipients)

        if self.type == EmailAddressType.MAILINGLIST:
            return send_message(message, self.recipients)

        raise NotImplementedError()
```
]
]

---

## .dimmed[The trivial implementation]

- A lot of logic is embedded in the `send` method, leading to brittleness.
- The logic is not easy to extend for new kinds of mailboxes.
- This approach needs a lot of validation logic, most of which has not been implemented here.
- The use of optional fields and parameters requires documentation to be written, maintained, and used when required.

---

## The trivial implementation with two classes

.columns[
.column[
```py
class Mailbox:
    id: UUID
    addr: str
    pwd_hash: str

    def send(
        self,
        message: str,
        recipients: tuple[str, ...],
    ):
        return send_message(message, recipients)
```
]
.column[
```py
class MailingList:
    id: UUID
    addr: str
    recipients: tuple[str, ...]

    def send(
        self,
        message: str,
    ):
        return send_message(message, self.recipients)
```
]
]

- Code is duplicated in two distinct implementations.
- Any changes required to one implementation may require changes to the other implementation.
- Implementations can drift over time.

---

## Simple subclassing

```py
class EmailAddress:
    id: UUID
    addr: str
```

.columns[
.column[
```py
    class Mailbox(EmailAddress):
        pwd_hash: str

        def send(
            self,
            message: str,
            recipients: list[str],
        ):
            return send_message(message, recipients)
```
]
.column[
```py
    class MailingList(EmailAddress):
        recipients: list[str]

        def send(
            self,
            message: str,
        ):
            return send_message(message, self.recipients)
```
]
]

---

## .dimmed[Simple subclassing]

Say something!

---

## Composition

```py
class EmailAddress:
    id: UUID
    addr: str
```

.columns[
.column[
```py
    class Mailbox:
        account: EmailAddress
        pwd_hash: str

        def send(
            self,
            message: str,
            recipients: tuple[str, ...],
        ):
            return send_message(message, recipients)
```
]
.column[
```py
    class MailingList:
        account: EmailAddress
        recipients: tuple[str, ...]

        def send(
            self,
            message: str,
        ):
            return send_message(message, self.recipients)
```
]
]

---

## .dimmed[Composition]

Say something!

---

## Nominal subtyping

```py
class EmailAddress(abc.ABC):
    id: UUID
    addr: str

    @abc.abstractmethod
    def send(
        self,
        message: str,
        *args,
        **kwargs,
    ): ...
```

.columns[
.column[
```py
    class Mailbox(EmailAddress):
        pwd_hash: str

        def send(
            self,
            message: str,
            recipients: tuple[str, ...],
        ):
            return send_message(message, recipients)
```
]
.column[
```py
    class MailingList(EmailAddress):
        recipients: tuple[str, ...]

        def send(
            self,
            message: str,
        ):
            return send_message(message, self.recipients)
```
]
]

---

## .dimmed[Nominal subtyping]

Say something!

---

## A different syntax for nominal subtyping

```py
class EmailAddress(metaclass=abc.ABCMeta):
    id: UUID
    addr: str

    @abc.abstractmethod
    def send(
        self,
        message: str,
        *args,
        **kwargs,
    ): ...
```

.columns[
.column[
```py
    @EmailAddress.register
    class Mailbox:
        pwd_hash: str

        def send(
            self,
            message: str,
            recipients: tuple[str, ...],
        ):
            return send_message(message, recipients)
```
]
.column[
```py
    @EmailAddress.register
    class MailingList:
        recipients: tuple[str, ...]

        def send(
            self,
            message: str,
        ):
            return send_message(message, self.recipients)
```
]
]

---

## .dimmed[A different syntax for nominal subtyping]

Say something!

---

## Structural subtyping

```py
@typing.runtime_checkable
class EmailAddress(typing.Protocol):
    def send(
        self,
        message: str,
        *args,
        **kwargs,
    ): ...
```

.columns[
.column[
```py
    class Mailbox:
        id: UUID
        addr: str
        pwd_hash: str

        def send(
            self,
            message: str,
            recipients: tuple[str, ...],
        ):
            return send_message(message, recipients)
```
]
.column[
```py
    class MailingList:
        id: UUID
        addr: str
        recipients: tuple[str, ...]

        def send(
            self,
            message: str,
        ):
            return send_message(message, self.recipients)
```
]
]

---

## .dimmed[Structural subtyping]

Say something!

---

class: center, middle

# The end
