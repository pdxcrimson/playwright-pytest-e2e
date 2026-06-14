from dataclasses import dataclass

from faker import Faker

fake = Faker()


@dataclass
class CheckoutInfo:
    first_name: str
    last_name: str
    postal_code: str


@dataclass
class UserProfile:
    username: str
    first_name: str
    last_name: str
    email: str
    postal_code: str


def make_checkout_info() -> CheckoutInfo:
    """Generate realistic checkout info for form-fill tests."""
    return CheckoutInfo(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        postal_code=fake.postcode(),
    )


def make_user_profile() -> UserProfile:
    first = fake.first_name()
    last = fake.last_name()
    return UserProfile(
        username=f"{first.lower()}.{last.lower()}{fake.numerify('##')}",
        first_name=first,
        last_name=last,
        email=fake.email(),
        postal_code=fake.postcode(),
    )


def make_postal_code(country: str = "US") -> str:
    """Generate a postal code for a specific country locale."""
    localized = Faker({"US": "en_US", "GB": "en_GB", "DE": "de_DE"}.get(country, "en_US"))
    return localized.postcode()
