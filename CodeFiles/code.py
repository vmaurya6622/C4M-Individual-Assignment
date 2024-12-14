from fhirpy import SyncFHIRClient
import json
import requests

# Step 1: Creating Patient resources list that I am going to use
patients = []  # Initialize as an empty list
conditions = []  # Initialize as an empty list
observations = []  # Initialize as an empty list
medication_requests = []  # Initialize as an empty list
practitioners = []  # Initialize as an empty list
FamilyMemberHistory = []  # Ensure this is initialized correctly
MedicationRequests = []  # Ensure this is initialized correctly
Appointments = []  # Initialize as an empty list
DiagnosticReports = []  # Initialize as an empty list
Organizations = []  # Initialize as an empty list
Medications = []  # Initialize as an empty list
Devices = []  # Initialize as an empty list


# Create a FHIR client instance using the public HAPI FHIR server
client = SyncFHIRClient("http://hapi.fhir.org/baseR4")


# Helper function to create a patient
def create_patient(family_name, given_name, gender, birth_date):
    patient = client.resource(
        "Patient",
        name=[{"family": family_name, "given": [given_name]}],
        gender=gender,
        birthDate=birth_date,
    )
    patient.save()
    return patient


patient_data = [
    ("Maurya", "Rohan", "male", "1995-01-01"),
    ("John", "Micheal", "male", "1982-02-02"),
    ("Tiwari", "Harish", "male", "1987-03-03"),
]

for family, given, gender, dob in patient_data:
    patient = create_patient(family, given, gender, dob)
    patients.append(patient)
    print(f"Patient {given} {family} created with ID: {patient['id']}")

# Step 2: List the patients with serial numbers
print("\nList of Patients:")
for i, patient in enumerate(patients):
    patient_name = patient.name[0]["given"][0] + " " + patient.name[0]["family"]
    print(f"{i + 1}. {patient_name}, ID: {patient['id']}")


# Fetch and save patient data
def fetch_and_save_patient_data(patient):
    patient_id = patient["id"]
    url = f"http://hapi.fhir.org/baseR4/Patient/{patient_id}"
    response = requests.get(url)

    if response.status_code == 200:
        fetched_patient = response.json()
        print("Fetched Patient Data:")
        print(json.dumps(fetched_patient, indent=4))

        given_name = (
            fetched_patient["name"][0]["given"][0]
            if fetched_patient["name"]
            else "Unknown"
        )
        family_name = (
            fetched_patient["name"][0]["family"]
            if fetched_patient["name"]
            else "Unknown"
        )

        file_name = f"{fetched_patient['id']}_{given_name}_{family_name}.json".replace(
            " ", "_"
        )
        try:
            with open(file_name, "w") as json_file:
                json.dump(fetched_patient, json_file, indent=4)
            print(f"Patient data saved to {file_name}")
        except Exception as e:
            print(f"Error saving patient data to file: {e}")
    else:
        print(f"Error fetching patient data: {response.status_code} - {response.text}")


while True:
    print("\nEnter 1 to update the data on the server.")
    print("Enter 2 to fetch and save the data in the form of JSON.")
    print("Enter 3 to move on.")
    print("Enter 4 to exit.")
    inp = int(input("Enter Input Here: "))
    inp += 1
    if inp == 1:
        print(
            "Upload operation is not defined separately, as patient data is saved on creation."
        )

    elif inp == 2:
        serial_number = (
            int(
                input(
                    "\nEnter the serial number of the patient whose data you want to update: "
                )
            )
            - 1
        )
        selected_patient = patients[serial_number]
        new_given_name = input(
            f"Enter new given name for {selected_patient.name[0]['given'][0]} (leave blank to keep the same): "
        )
        new_family_name = input(
            f"Enter new family name for {selected_patient.name[0]['family']} (leave blank to keep the same): "
        )
        new_gender = input(
            f"Enter new gender for {selected_patient.gender} (leave blank to keep the same): "
        )
        new_birth_date = input(
            f"Enter new birth date for {selected_patient.birthDate} (leave blank to keep the same): "
        )
        if new_given_name:
            selected_patient.name[0]["given"][0] = new_given_name
        if new_family_name:
            selected_patient.name[0]["family"] = new_family_name
        if new_gender:
            selected_patient.gender = new_gender
        if new_birth_date:
            selected_patient.birthDate = new_birth_date

        try:
            selected_patient.save()
            print(f"Patient data updated successfully. New data: {selected_patient}")
        except Exception as e:
            print(f"Error updating patient data: {e}")

    elif inp == 3:
        serial_number = (
            int(
                input(
                    "\nEnter the serial number of the patient whose data you want to save: "
                )
            )
            - 1
        )
        selected_patient = patients[serial_number]
        fetch_and_save_patient_data(selected_patient)

    elif inp == 4:
        print("Moving on to the next step...\n\n")
        break

    else:
        print("\nWrong Input.\n")

# Practitioner Resource Implementation
doctor_wilson = client.resource(
    "Practitioner", name=[{"family": "Wilson", "given": ["Emily"]}], gender="female"
)
practitioners.append(doctor_wilson)
try:
    doctor_wilson.save()
    print(f"Practitioner created with ID: {doctor_wilson['id']}")
except Exception as e:
    print(f"Error creating practitioner: {e}")

# Condition Implementation
selected_patient = patients[0]
condition = client.resource(
    "Condition",
    subject={"reference": f'Patient/{selected_patient["id"]}'},
    code={
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "44054006",
                "display": "Type 2 Diabetes Mellitus",
            }
        ]
    },
    clinicalStatus={
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": "active",
                "display": "Active",
            }
        ]
    },
)
conditions.append(condition)
try:
    condition.save()
    print(
        f"Condition (Diabetes) created with ID: {condition['id']} for {selected_patient['id']}"
    )
except Exception as e:
    print(f"Error creating condition: {e}")

# Observation Implementation
new_observation = client.resource(
    "Observation",
    status="final",
    category=[
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                    "code": "laboratory",
                }
            ]
        }
    ],
    code={
        "coding": [
            {
                "system": "http://loinc.org",
                "code": "4548-4",
                "display": "Hemoglobin A1c/Hemoglobin.total in Blood",
            }
        ]
    },
    subject={"reference": f'Patient/{selected_patient["id"]}'},
    valueQuantity={"value": 7.0, "unit": "%"},
    effectiveDateTime="2024-09-28T00:00:00Z",
)
observations.append(new_observation)
try:
    new_observation.save()
    print(f"Observation (HbA1c) created with ID: {new_observation['id']}")
except Exception as e:
    print(f"Error creating observation: {e}")

# Medication Request Implementation
medication_request = client.resource(
    "MedicationRequest",
    subject={"reference": f'Patient/{selected_patient["id"]}'},
    medicationCodeableConcept={
        "coding": [
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "860975",
                "display": "Metformin 500mg tablet",
            }
        ]
    },
    dosageInstruction=[{"text": "Take 1 tablet twice daily"}],
)
medication_requests.append(medication_request)
try:
    medication_request.save()
    print(f"MedicationRequest created with ID: {medication_request['id']}")
except Exception as e:
    print(f"Error creating MedicationRequest: {e}")


# FamilyMemberHistory Resource Implementation
family_member_history = client.resource(
    "FamilyMemberHistory",
    patient={"reference": f'Patient/{selected_patient["id"]}'},
    relationship={
        "coding": [
            {
                "system": "http://hl7.org/fhir/family-relationship",
                "code": "father",
                "display": "Father",
            }
        ]
    },
    name="John Doe",
    bornDate="1970-01-01",
    note=[{"text": "Father has a history of hypertension."}],
    condition=[
        {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "431855005",
                    "display": "Hypertension",
                }
            ]
        }
    ],
)

FamilyMemberHistory.append(family_member_history)

try:
    family_member_history.save()
    print(f"FamilyMemberHistory created with ID: {family_member_history['id']}")
except Exception as e:
    print(f"Error creating FamilyMemberHistory: {e}")


# MedicationRequest Implementation
medication_request = client.resource(
    "MedicationRequest",
    subject={"reference": f'Patient/{selected_patient["id"]}'},
    medicationCodeableConcept={
        "coding": [
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "860975",
                "display": "Metformin 500mg tablet",
            }
        ]
    },
    dosageInstruction=[{"text": "Take 1 tablet twice daily"}],
)

MedicationRequests.append(medication_request)

try:
    medication_request.save()
    print(f"MedicationRequest created with ID: {medication_request['id']}")
except Exception as e:
    print(f"Error creating MedicationRequest: {e}")


# Appointment Implementation
appointment = client.resource(
    "Appointment",
    status="booked",
    serviceType=[
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/service-types",
                    "code": "consult",
                    "display": "Consultation",
                }
            ]
        }
    ],
    start="2024-09-29T10:00:00Z",
    end="2024-09-29T11:00:00Z",
    participant=[
        {
            "actor": {"reference": f'Patient/{selected_patient["id"]}'},
            "status": "accepted",
        }
    ],
)

Appointments.append(appointment)

try:
    appointment.save()
    print(f"Appointment created with ID: {appointment['id']}")
except Exception as e:
    print(f"Error creating Appointment: {e}")


# DiagnosticReport Implementation
diagnostic_report = client.resource(
    "DiagnosticReport",
    status="final",
    category=[
        {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "57027-8",
                    "display": "Lab Report",
                }
            ]
        }
    ],
    subject={"reference": f'Patient/{selected_patient["id"]}'},
    effectiveDateTime="2024-09-28T00:00:00Z",
    result=[{"reference": f'Observation/{new_observation["id"]}'}],
)

DiagnosticReports.append(diagnostic_report)

try:
    diagnostic_report.save()
    print(f"DiagnosticReport created with ID: {diagnostic_report['id']}")
except Exception as e:
    print(f"Error creating DiagnosticReport: {e}")


# Organization Implementation
organization = client.resource(
    "Organization",
    name="Health Care Organization",
    type=[
        {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                    "code": "prov",
                    "display": "Provider",
                }
            ]
        }
    ],
)

Organizations.append(organization)

try:
    organization.save()
    print(f"Organization created with ID: {organization['id']}")
except Exception as e:
    print(f"Error creating Organization: {e}")



# Medication Implementation
medication = client.resource(
    "Medication",
    code={
        "coding": [
            {
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": "860975",
                "display": "Metformin 500mg tablet",
            }
        ]
    },
)

Medications.append(medication)

try:
    medication.save()
    print(f"Medication created with ID: {medication['id']}")
except Exception as e:
    print(f"Error creating Medication: {e}")


# Device Implementation
device = client.resource(
    "Device",
    udiCarrier=[
        {
            "deviceIdentifier": "123456789",
            "jurisdiction": "http://hl7.org/fhir/udi-issuer",
        }
    ],
    status="active",
    type={
        "coding": [
            {
                "system": "http://snomed.info/sct",
                "code": "123456",
                "display": "Example Device",
            }
        ]
    },
)

Devices.append(device)

try:
    device.save()
    print(f"Device created with ID: {device['id']}")
except Exception as e:
    print(f"Error creating Device: {e}")

# Fetch and print updated patient details
patient = client.resources("Patient").search(_id=selected_patient["id"]).first()
if patient:
    patient_name = patient.name[0]["given"][0] + " " + patient.name[0]["family"]
    patient_gender = patient.gender
    patient_birth_date = patient.birthDate

    print(
        f"\nUpdated Patient ID: {patient['id']}, Name: {patient_name}, Gender: {patient_gender}, Date of Birth: {patient_birth_date}"
    )
else:
    print("Patient not found.")


# Function to create a FHIR Bundle containing all resources
def create_bundle(resources):
    """Create a FHIR Bundle containing all resources."""
    bundle = {"resourceType": "Bundle", "type": "transaction", "entry": []}

    for resource in resources:
        entry = {
            "fullUrl": f"http://hapi.fhir.org/baseR4/{resource['resourceType']}/{resource['id']}",
            "resource": resource,
            "request": {"method": "POST", "url": resource["resourceType"]},
        }
        bundle["entry"].append(entry)

    return bundle


# Collect all resources into a single list
all_resources = (
    patients  # This is a list of resources
    + practitioners  # This is a list of resources
    + conditions  # This is a list of resources
    + observations  # This is a list of resources
    + medication_requests  # This is a list of resources
    + FamilyMemberHistory  # Fix to reference the correct list
    + MedicationRequests  # This is a list of resources
    + Appointments  # This is a list of resources
    + DiagnosticReports  # This is a list of resources
    + Organizations  # This is a list of resources
    + Medications  # This is a list of resources
    + Devices  # This is a list of resources
)


# Create the FHIR Bundle
bundle = create_bundle(all_resources)

# Save the bundle to a JSON file
with open("JSON_Bundle.json", "w") as json_file:
    json.dump(bundle, json_file, indent=4)
print("JSON bundle created and saved as JSON_Bundle.json")
