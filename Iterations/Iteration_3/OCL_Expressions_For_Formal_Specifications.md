# OCL Constraints Documentation

## Unique Offerings
### Description
Offerings must be unique. Multiple offerings on the same day and time slot must be offered at different locations.

### Constraint
```ocl
context Offering
inv: Offering.allInstances()->forAll(o1, o2 |
    o1 <> o2 implies 
    (o1.day <> o2.day or o1.timeSlot <> o2.timeSlot or o1.location <> o2.location)
)
ocl```
## Underage Clients with Guardians
### Description
Any client under the age of 18 must be accompanied by an adult guardian.

### Constraint
```ocl
context Client
inv: self.age < 18 implies self.guardian->notEmpty()

## Instructor Availability for Offerings
### Description
The city associated with an offering must be one of the cities indicated in the instructor's availabilities.

### Constraint
```ocl
context Offering
inv: self.instructor.availabilities->exists(a | a.city = self.city)

## Unique Client Bookings
### Description
A client cannot have multiple bookings on the same day and time slot.

### Constraint
```ocl
context Client
inv: self.bookings->forAll(b1, b2 | 
    b1 <> b2 implies (b1.day <> b2.day or b1.timeSlot <> b2.timeSlot)
)
