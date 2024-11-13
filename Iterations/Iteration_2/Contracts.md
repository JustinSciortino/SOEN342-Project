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


# Contract CO3: Register Client

**Operation: register_client(name: String, password: String, phone_number: String)**

**Cross References: Use case Login/Register/Logout**  

**Pre-conditions:**  

1. A session with the database exists and is active
2. The User, Client, Instructor and Admin tables has been created in the database
3. The name parameter is a non-empty string
4. The password parameter is a non-empty string
5. The phone_number parameter is non-empty string

**Post-conditions:**  

1. A Client instance client was created. (instance creation)
2. Client instance is added to the User and Client database tables


# Contract CO4: Delete Instructor or Client 

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
3. Client association with minor broken (association broken)
4. Client minors deleted (instance deletion)
3. If a Client is deleted, delete all client (and associated minors) bookings and make Offering availble if it was previously Not-Available (instance modification)
5. Client (and associated minors) bookings are deleted (instance deletion and association broken)
4. If a Instructor was deleted, break all associated Offerings (association broken), delete all associated Offerings (instance deletion), delete client bookings associated with any deleted Offering


# Contract CO5: Create Offering 

**Operation: create_offering(lesson: Lesson, instructor: Instructor)**

**Cross References: Create Offering**  

**Pre-conditions:**  

1. A session with the database exists and is active
2. The lesson and instructor parameters are non-empty and are of valid type
3. No time conflicts exists between the Lesson's timeslot and the instructors schedule of offerings they will teach

**Post-conditions:**  

1. Offering instance offering is created (instance creation)
2. Association formed between Offering and Lesson as well as Offering and Instructor (association formed)

---

## Contract CO6: Remove Instructor from Offering

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

## Contract CO7: Create Booking for Client

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

## Contract CO8: Cancel Client Booking

**Operation**: `cancel_booking(self, booking_id: int)`

**Cross References**: Cancel Booking

### Pre-conditions:
- A session with the database exists and is active.
- The `booking_id` parameter is a non-empty parameter.

### Post-conditions:
- The Booking association with Client is broken (association broken)
- The Booking association with Offering is broken and the Booking is removed from the Offering (assoication broken) 
- The `Booking` instance is deleted

---

# Contract C09: Create Lesson

**Operation: create_lesson(location: Location, capacity: int, timeslot: Timeslot, lesson_type: LessonType, specialization: SpecializationType)**

**Cross References: Create Lesson**  

**Pre-conditions:**  

1. A session with the database exists and is active
2. The location parameter is a valid existing Location instance
3. The capacity is a valid integer, greater than zero and less than or equal to the Location instance capacity
4. The timeslot parameter is a valid Timeslot instance
5. The timeslot instance does not conflict with the Location instance's Schedule instance consisting of a list of Timeslot instances
6. The offering_type parameter is a non-empty and a valid type of LessonType
7. The specialization parameter is a non-empty and a valid type of SpecializationType 

**Post-conditions:**  

1. Offering instance offering is created (instance creation)
2. Association formed between offering and timeslot (association formed)
3. Association formed between offering and location (association formed)
4. offering.type was set to offering_type (attribute modification)
5. offering.specialization was set to specialization (attribute modification)
6. timeslot is added to the Location instance's Schedule.timeslots (attribute modification)

