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
