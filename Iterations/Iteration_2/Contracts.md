# Contracts

## Contract CO7: Assign Instructor to Offering

**Operation**: `assign_instructor_to_offering(self, instructor, offering: Offering)`

**Cross References**: Assigning Instructor to Teach Offering

### Pre-conditions:
- A session with the database exists and is active.
- The `offering` parameter is a valid Offering instance.
- The `instructor` parameter is a valid Instructor instance.
- The `offering` does not already have an assigned instructor.

### Post-conditions:
- The `instructor_id` attribute of the `offering` is updated to reference the `instructor`.
- The `instructor.offerings` list is updated to include the `offering`.
- Changes are committed to the database.
- If an error occurs, the transaction is rolled back, and a `ValueError` is raised.

---

## Contract CO8: Get Available Offerings for Instructor

**Operation**: `get_available_offerings_for_instructor(self, cities, specializations)`

**Cross References**: Instructor Viewing Available Offerings

### Pre-conditions:
- A session with the database exists and is active.
- The `cities` parameter is a non-empty list of valid city names.
- The `specializations` parameter is a non-empty list of valid SpecializationType values.
- The Offering table has at least one offering that matches the `cities` and `specializations` criteria.
- The `offering.instructor_id` is set to `None` (i.e., the offering is not yet assigned to any instructor).

### Post-conditions:
- A list of available `Offering` instances is returned that match the given `cities` and `specializations` and are not yet assigned to any instructor.

---

## Contract CO9: Remove Instructor from Offering

**Operation**: `remove_instructor_from_offering(self, instructor, offering: Offering)`

**Cross References**: Remove Instructor from Teaching Offering

### Pre-conditions:
- A session with the database exists and is active.
- The `offering` parameter is a valid Offering instance.
- The `instructor` parameter is a valid Instructor instance.
- The `offering.instructor_id` references the `instructor.id`.

### Post-conditions:
- The `instructor_id` attribute of the `offering` is set to `None`.
- The `instructor.offerings` list is updated to remove the `offering`.
- All associated `Booking` instances are deleted (for both minors and clients).
- Changes are committed to the database.
- If an error occurs, the transaction is rolled back, and a `ValueError` is raised.

---

## Contract CO10: Create Booking for Client

**Operation**: `create_booking(self, client: Client, offering: Offering, minor_id: int = None)`

**Cross References**: Booking Creation

### Pre-conditions:
- A session with the database exists and is active.
- The `client` parameter is a valid Client instance.
- The `offering` parameter is a valid Offering instance.
- If provided, the `minor_id` corresponds to a valid Minor instance.

### Post-conditions:
- A `Booking` instance is created and linked to the `client` and `offering`.
- The `offering` is updated to include the new booking.
- If `minor_id` is provided, the booking is also linked to the corresponding Minor instance.
- The new booking is committed to the database.
- If an error occurs, the transaction is rolled back, and no booking is created.

---

## Contract CO11: Get Client Bookings

**Operation**: `get_client_bookings(self, client: Client)`

**Cross References**: View Bookings

### Pre-conditions:
- A session with the database exists and is active.
- The `client` parameter is a valid Client instance.

### Post-conditions:
- Returns a list of all `Booking` instances associated with the `client`.

---

## Contract CO12: Cancel Client Booking

**Operation**: `cancel_booking(self, client: Client, booking: Booking, minor_id: int = None)`

**Cross References**: Cancel Booking

### Pre-conditions:
- A session with the database exists and is active.
- The `client` parameter is a valid Client instance.
- The `booking` parameter is a valid Booking instance.
- If provided, the `minor_id` corresponds to a valid Minor instance linked to the booking.

### Post-conditions:
- The `Booking` instance is removed from the `client` and `offering`.
- If a `minor_id` is provided, the booking is also removed from the Minor instance.
- The `Booking` instance is either deleted or marked as canceled based on business rules.
- The changes are committed to the database.
- If an error occurs, the transaction is rolled back, and the booking remains active.

---

## Contract CO13: Get Minor Bookings

**Operation**: `get_minor_bookings(self, minor_id: int)`

**Cross References**: View Minor Bookings

### Pre-conditions:
- A session with the database exists and is active.
- The `minor_id` is a valid ID corresponding to a Minor instance.

### Post-conditions:
- Returns a list of all `Booking` instances associated with the `minor_id`.


