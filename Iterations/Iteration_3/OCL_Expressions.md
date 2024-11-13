# Login

**Operation**: `login(name, password, phone_number: String = None)`

**Context**: `System::login(name: String, password: String, phone_number: String) : User`
- **Preconditions:**
  - `self.session.isActive()`
  - `self.tables -> includesAll(Set{'User', 'Client', 'Instructor', 'Admin'})`
  - `not name.isEmpty()`
  - `not password.isEmpty()`
  - `phone_number = null or (phone_number.size() = 10 and phone_number.matches('[0-9]+'))`
- **Postconditions:**
  - `result.oclIsTypeOf(Client) implies result.userType = 'client'`
  - `result.oclIsTypeOf(Instructor) implies result.userType = 'instructor'`
  - `result.oclIsTypeOf(Admin) implies result.userType = 'admin'`
  - `result.isAuthenticated = true`

---

# Register Instructor

**Operation**: `register_instructor(name: String, password: String, phone_number: String, specialization: Set(SpecializationType), available_cities: Set(String))`

**Context**: `System::register_instructor(name: String, password: String, phone_number: String, specialization: Set(SpecializationType), available_cities: Set(String)) : Instructor`
- **Preconditions:**
  - `self.session.isActive()`
  - `self.tables -> includesAll(Set{'User', 'Client', 'Instructor', 'Admin'})`
  - `not name.isEmpty()`
  - `not password.isEmpty()`
  - `phone_number.size() = 10 and phone_number.matches('[0-9]+')`
  - `specialization->forAll(s | s.oclIsTypeOf(SpecializationType))`
  - `available_cities->notEmpty() and available_cities->forAll(city | city.oclIsTypeOf(String))`
- **Postconditions:**
  - `result.oclIsTypeOf(Instructor)`
  - `User.allInstances()->includes(result) and Instructor.allInstances()->includes(result)`

---

# Register Client

**Operation**: `register_client(name: String, password: String, phone_number: String)`

**Context**: `System::register_client(name: String, password: String, phone_number: String) : Client`
- **Preconditions:**
  - `self.session.isActive()`
  - `self.tables -> includesAll(Set{'User', 'Client', 'Instructor', 'Admin'})`
  - `not name.isEmpty()`
  - `not password.isEmpty()`
  - `not phone_number.isEmpty()`
- **Postconditions:**
  - `result.oclIsTypeOf(Client)`
  - `User.allInstances()->includes(result) and Client.allInstances()->includes(result)`

---

# Delete Instructor or Client

**Operation**: `delete_user(name: String, id: int)`

**Context**: `System::delete_user(name: String, id: Integer)`
- **Preconditions:**
  - `self.session.isActive()`
  - `self.tables -> includesAll(Set{'User', 'Client', 'Instructor', 'Admin'})`
  - `not name.isEmpty() or id > 0`
  - `User.allInstances()->exists(u | u.name = name or u.id = id)`
- **Postconditions:**
  - `not User.allInstances()->exists(u | u.name = name or u.id = id)`
  - Additional conditions based on user type.

---

# Create Offering

**Operation**: `create_offering(lesson: Lesson, instructor: Instructor)`

**Context**: `System::create_offering(lesson: Lesson, instructor: Instructor) : Offering`
- **Preconditions:**
  - `self.session.isActive()`
  - `lesson <> null and lesson.oclIsTypeOf(Lesson)`
  - `instructor <> null and instructor.oclIsTypeOf(Instructor)`
  - `not instructor.schedule->exists(o | o.timeslot.overlaps(lesson.timeslot))`
- **Postconditions:**
  - result.oclIsTypeOf(Offering)
  - `result.lesson = lesson and result.instructor = instructor`

---

# Remove Instructor from Offering

**Operation**: `remove_instructor_from_offering(self, instructor: Instructor, offering: Offering)`

**Context**: `System::remove_instructor_from_offering(instructor: Instructor, offering: Offering)`
- **Preconditions:**
  - `self.session.isActive()`
  - `offering <> null and offering.oclIsTypeOf(Offering)`
  - `instructor <> null and instructor.oclIsTypeOf(Instructor)`
  - `offering.instructor.id = instructor.id`
- **Postconditions:**
  - `offering.instructor = null`
  - `instructor.offerings->excludes(offering)`
  - `Booking.allInstances()->forAll(b | b.offering <> offering)`

---

# Create Booking for Client

**Operation**: `create_booking(self, client: Client, offering: Offering, minor_id: int = None)`

**Context**: `System::create_booking(client: Client, offering: Offering, minor_id: Integer = null) : Booking`

- **Preconditions:**
  - `self.session.isActive()`
  - `client <> null and client.oclIsTypeOf(Client)`
  - `offering <> null and offering.oclIsTypeOf(Offering)`
  - `minor_id = null or Minor.allInstances()->exists(m | m.id = minor_id)`

- **Postconditions:**
  - `result.oclIsTypeOf(Booking)`
  - `offering.bookings->includes(result) and client.bookings->includes(result)`
  - `if minor_id <> null then result.minor.id = minor_id endif`

---

# Cancel Client Booking

**Operation**: `cancel_booking(self, booking_id: int)`

**Context**: `System::cancel_booking(booking_id: Integer)`
- **Preconditions:**
  - `self.session.isActive()`
  - `Booking.allInstances()->exists(b | b.id = booking_id)`
- **Postconditions:**
  - `not Booking.allInstances()->exists(b | b.id = booking_id)`

---

# Create Lesson

**Operation**: `create_lesson(location: Location, capacity: int, timeslot: Timeslot, lesson_type: LessonType, specialization: SpecializationType)`

**Context**: `System::create_lesson(location: Location, capacity: Integer, timeslot: Timeslot, lesson_type: LessonType, specialization: SpecializationType) : Lesson`

- **Preconditions:**
  - `self.session.isActive()`
  - `location.oclIsTypeOf(Location)`
  - `capacity > 0 and capacity <= location.capacity`
  - `timeslot.oclIsTypeOf(Timeslot) and not location.schedule.timeslots->exists(t | t.overlaps(timeslot))`
  - `lesson_type <> null and lesson_type.oclIsTypeOf(LessonType)`
  - `specialization <> null and specialization.oclIsTypeOf(SpecializationType)`

- **Postconditions:**
  - `result.oclIsTypeOf(Lesson)`
  - `result.timeslot = timeslot and result.location = location`
  - `result.type = lesson_type and result.specialization = specialization`
  - `location.schedule.timeslots->includes(timeslot)`

