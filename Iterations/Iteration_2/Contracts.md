# Contracts

# Contract CO1: Login

**Operation: login(name:String, password:String, phone_number: String = None)**

**Cross References: Use case Login/Register/Logout**  

**Pre-conditions:**  

1. A session with the database exists and is active
2. The User, Client, Instructor and Admin tables has been created in the database
3. The name parameter is a non-empty string
4. The password parameter is a non-empty string
5. The phone_number parameter (only for Instructor logins) is a 10-digit string

**Post-conditions:**  

1. Returns a Client object if the user type is client
2. Returns an Instructor object if the user type is instructor
3. Returns an Admin object is the user type is Admin
4. User is authenticated and is shown their user type menu option


# Contract CO2: Register Instructor

**Operation: register_instructor(name: String, password: String, phone_number: String, specialization: list[SpecializationType], available_cities: list[String])**

**Cross References: Use case Login/Register/Logout**  

**Pre-conditions:**  

1. A session with the database exists and is active
2. The User, Client, Instructor and Admin tables has been created in the database
3. The name parameter is a non-empty string
4. The password parameter is a non-empty string
5. The phone_number parameter (only for Instructor logins) is a 10-digit string
6. The specialization types are of type SpecializationType
7. The available_cities parameter is a non-empty list of strings

**Post-conditions:**  

1. An Instructor instance instructor was created. (instance creation)
2. Instructor instance is added to the User and Instructor database tables


# Contract CO3: Register Admin

**Operation: register_admin(name: String, password: String)**

**Cross References: Use case Login/Register/Logout**  

**Pre-conditions:**  

1. A session with the database exists and is active
2. The User, Client, Instructor and Admin tables has been created in the database
3. The name parameter is a non-empty string
4. The password parameter is a non-empty string
5. There does not exists another administrator for the organization

**Post-conditions:**  

1. An Admin instance admin was created. (instance creation)
2. Admin instance is added to the User and Admin database tables


# Contract CO4: Register Client INCOMPLETE

**Operation: register_client(name: String, password: String)**

**Cross References: Use case Login/Register/Logout**  

**Pre-conditions:**  

1. A session with the database exists and is active
2. The User, Client, Instructor and Admin tables has been created in the database
3. The name parameter is a non-empty string
4. The password parameter is a non-empty string

**Post-conditions:**  

1. A Client instance client was created. (instance creation)
2. Client instance is added to the User and Client database tables


# Contract CO5: Delete Instructor or Client 

**Operation: delete_user(name: String, id: int)**

**Cross References: Delete Instructor/Client Account**  

**Pre-conditions:**  

1. A session with the database exists and is active
2. The User, Client, Instructor and Admin tables has been created in the database
3. The name parameter or id parameter is non-empty string or integer
4. User is a Client or Instructor instance
5. Client/Instructor to be deleted exists in the system

**Post-conditions:**  

1. Client/Instructor instance is deleted from the system. (instance deletion)
2. Client/Instructor instance is deleted from the database
3. Association between Client/Instructor and Booking/Offering broken. (association broken)
4. Offering instance associated with the Instructor is cancelled and all bookings instance associated with the Offering instance are cancelled (association broken)
5. All Booking instances associated with the Client are broken (association broken) and deleted (instance deletion)


# Contract CO6: Create Offering 

**Operation: create_offering(location: Location, capacity: int, timeslot: Timeslot, offering_type: OfferingType, specialization: SpecializationType)**

**Cross References: Create Offering**  

**Pre-conditions:**  

1. A session with the database exists and is active
2. The location parameter is a valid existing Location instance
3. The capacity is a valid integer, greater than zero and less than or equal to the Location instance capacity
4. The timeslot parameter is a valid Timeslot instance
5. The timeslot instance does not conflict with the Location instance's Schedule instance consisting of a list of Timeslot instances
6. The offering_type parameter is a non-empty and a valid type of OfferingType
7. The specialization parameter is a non-empty and a valid type of SpecializationType

**Post-conditions:**  

1. Offering instance offering is created (instance creation)
2. Association formed between offering and timeslot (association formed)
3. Association formed between offering and location (association formed)
4. offering.type was set to offering_type (attribute modification)
5. offering.specialization was set to specialization (attribute modification)
6. timeslot is added to the Location instance's Schedule.timeslots (attribute modification)


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


