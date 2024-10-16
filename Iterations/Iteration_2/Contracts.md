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
