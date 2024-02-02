from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django import forms
from decimal import Decimal
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify


# class UserProfile(models.Model):

#     user = models.OneToOneField(User, on_delete=models.CASCADE)
    # additional info of the user


class Contract(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contractee = models.CharField(max_length=200)
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name="service")
    start_date = models.CharField(max_length=200)
    end_date = models.CharField(max_length=200)

class Service(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    virtual = models.ForeignKey('Virtual', on_delete=models.CASCADE)
    hanging_license = models.ForeignKey('HangingLicense', on_delete=models.CASCADE) 
    mail_forwarding = models.ForeignKey('MailForwarding', on_delete=models.CASCADE)
    mail_box = models.ForeignKey('MailBoxService', on_delete=models.CASCADE)
    copy_services = models.ForeignKey('CopyServices', on_delete=models.CASCADE)

class Mailbox(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Other mailbox properties

class Mail(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mailbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE)
    # Other mail properties

class Note(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mailbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE)
    # Other note properties

class Gift(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mailbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE)
    # Other gift properties

class Package(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mailbox = models.ForeignKey(Mailbox, on_delete=models.CASCADE)
    # Other package properties

class MailForwarding(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mailbox_number = models.ForeignKey('MailBoxService', on_delete=models.CASCADE)

class MailBoxService(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.ForeignKey('Company', on_delete=models.CASCADE, related_name="company_name") 
    owner_name = models.ForeignKey('Owner', on_delete=models.CASCADE) 
    additional_name = models.CharField(max_length=200)    
    eMail = models.EmailField(max_length=40, null=True)
    additional_email_address = models.EmailField(max_length=40, null=True)
    additional_company = models.CharField(max_length=200, null=True, blank=True)
    office = models.ForeignKey('Office', on_delete=models.CASCADE, related_name="office")	
    mail_box_number = models.CharField(max_length=200, unique=True)
    mail_forwarding = models.BooleanField(default=False)
    existing_mail = models.BooleanField(default=False) 
    new_mail = models.BooleanField(default=False)
    existing_package = models.BooleanField(default=False)
    new_package = models.BooleanField(default=False)
    existing_gift = models.BooleanField(default=False)
    new_gift = models.BooleanField(default=False)
    existing_note = models.BooleanField(default=False)
    new_note = models.BooleanField(default=False)

    def __str__(self):
        return f"Mailbox: {self.mail_box_number} and {self.additional_name} " \
            + f"with company:{self.company_name }\n owner: {self.owner_name}"

class CopyServices(models.Model): 
    
    QUALITY = [('standard', 'Standard'), ('premium', 'Premium'), ('specialty', 'Specialty')]
    COLOR = [('full_color', 'Full Color'), ('black_and_white', 'Black and White'), ('grayscale', 'Grayscale')]
    BINDING = [('stapled', 'Stapled'), ('spiral_bound', 'Spiral Bound'), ('booklet', 'Booklet')]
    ORDER_STATUS = [('processing', 'Processing'), ('completed', 'Completed'), ('shipped', 'Shipped'), ('Received', 'Received')]
    SIZE = [('8-1/2 x 11', 'Standard Letter 8-1/2 x 11'), ('8-1/2 x 14', 'Standard Legal 8-1/2 x 14'), ('11 x 17', '11 x 17')]
    DELIVERY = [('mailbox', 'Mailbox'), ('office', 'Office'), ('pickup_at_reception', 'Pickup at Reception'), 
                ('local_delivery', 'Local Delivery')]
    CODE = [('happy', 'Happy'), ('truth', 'Truth'), ('smile', 'Smile'), ('good', 'Good'), ('enjoy', 'Enjoy')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    price = models.DecimalField(max_digits=8, decimal_places=2)
    price_type = models.CharField(max_length=20, choices=QUALITY)
    paper_size = models.CharField(max_length=20, choices=SIZE)
    paper_quality =models.CharField(max_length=20, choices=QUALITY)
    color_option = models.CharField(max_length=20, choices=COLOR)
    binding_option = models.CharField(max_length=20, choices=BINDING)
    delivery_option = models.CharField(max_length=20, choices=DELIVERY)
    delivery_address = models.TextField(blank=True, null=True)
    deliver_date = models.DateTimeField(blank=True, null=True)
    additional_services = models.TextField(blank=True, null=True)
    payment_received = models.BooleanField(default=False)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS)
    comments = models.TextField(blank=True, null=True)
    discount_code = models.CharField(max_length=20, blank=True, null=True, choices=CODE)
    order_reference = models.CharField(max_length=20, unique=True)
    file_Upload = models.FileField(upload_to='uploads/', blank=True)
    quantity = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calculate the total_price based on price and quantity
        self.total_price = self.price * self.quantity

        super(CopyServices, self).save(*args, **kwargs)

    def __str__(self):
        return f"Copy Services by {self.user.username}({self.quantity} copies total price - {self.total_price})"
    
    def total_cost(self):
        return self.price * self.quantity

class Location(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    street_number = models.CharField(max_length=20, null=True)  # Field for street number
    street_name = models.CharField(max_length=200, null=True)    # Field for street name
    city = models.CharField(max_length=100, null=True)           # Field for city
    state = models.CharField(max_length=100, null=True)          # Field for state
    zip = models.CharField(max_length=20, null=True)     # Field for ZIP code
    address = models.CharField(max_length=100, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Concatenate the four fields into the 'employee' field
        self.address = f"{self.street_number} {self.street_name}{{\n}}{self.city}, {self.state} {self.zip}"

        super(Location, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name }\n{self.street_number} {self.street_name} \n{self.city}, {self.state}   {self.zip}"

# class Lease(models.Model):
#     
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     lessee = models.CharField(max_length=300)
#     company = models.ForeignKey('Company', on_delete=models.CASCADE)
#     owner = models.ForeignKey('Owner', on_delete=models.CASCADE)
#     employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
#     office_number = models.ForeignKey('Office', on_delete=models.CASCADE)
#     access_card = models.ForeignKey('AccessCard', on_delete=models.CASCADE)
#     rent = models.ForeignKey('Office', on_delete=models.CASCADE, related_name="lease_rent")
#     payment_period = models.ForeignKey('Office', on_delete=models.CASCADE, related_name="payment_period_lease")
#     term_lease = models.ForeignKey('Office', on_delete=models.CASCADE, related_name="term")  
#     lease_price_office = models.ForeignKey('Office', on_delete=models.CASCADE, related_name="lease_price")
#     start_date = models.ForeignKey('Office', on_delete=models.CASCADE, related_name="start_date")
#     end_date = models.ForeignKey('Office', on_delete=models.CASCADE, related_name="end_date")
#     sign_date = models.ForeignKey('Office', on_delete=models.CASCADE, related_name="sign_date")
#     contract_file = models.FileField(upload_to='contracts/')  

#     def get_lessee(self):
#         return f"{self.company}\n{self.owner}"
    
#     def calculate_duration(self):
#         if self.start_date is None or self.end_date is None:
#             return None

#         # Calculate the duration in days
#         duration = (self.end_date - self.start_date).days
#         return duration

#     def __str__(self):
#         duration = self.calculate_duration()
#         return f"{self.office_name}:  Contract Value:  ${self.lease_price_office} "\
#           +f"payable on: {self.end_date}  {self.get_lessee()} "\
#           +f"Contract duration: {duration} days from {self.start_date} to {self.end_date}"

class Suite(models.Model):
    SUITE_TYPE_CHOICES = [
        ('conventional', 'Conventional'),
        ('executive', 'Executive'),
    ]
    SUITE_NUMBER = [
        ('100', '100'), ('110', '110')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    building = models.ForeignKey(Location, on_delete=models.CASCADE, default="Unknown Building Identifier")
    suite_number = models.CharField(max_length=10, choices=SUITE_NUMBER)
    suite_type = models.CharField(max_length=15, choices=SUITE_TYPE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.suite_number

class Office(models.Model):
    OFFICE_TYPE_CHOICES = [
        ('window', 'Window'),
        ('interior', 'Interior'),
    ]

    OFFICE_CHOICES = [
        ('K1', 'K1'), ('K2', 'K2'), ('K3', 'K3'), ('K4', 'K4'), ('K5', 'K5'), ('K6', 'K6'), ('K7', 'K7'), 
        ('K8', 'K8'), ('K9', 'K9'), ('K10', 'K10'), ('K11', 'K11'), ('K12', 'K12'), ('K13', 'K13'), 
        ('K14', 'K14'), ('S1a', 'S1a'), ('S1b', 'S1b'), ('S2', 'S2'), ('S3', 'S3'), ('S4', 'S4'),        
        ('S5', 'S5'), ('S6', 'S6'), ('S7', 'S7'), ('S8', 'S8'), ('S9', 'S9'), ('S10', 'S10'),
        ('S11', 'S11'), ('S12', 'S12'), ('S13', 'S13'), ('S14', 'S14'), ('S15', 'S15'), ('S16', 'S16') 
    ]
    SCENARIOS = [
        ('one tenant lease', 'one tenant lease'), ('Joint Tenancy','Joint Tenancy'), ('Subletting','Subletting'), 
        ('Separate Leases','Separate Leases'), ('Cotenancy','Cotenancy'), 
        ('Room Rental Agreement','Room Rental Agreement')
    ]
    AMENITIES = [
        ('phone','phone'), ('fax','fax'), ('TV','TV'), ('Computer','Computer'), ('Projector','Projector'), 
        ('Secretary','Secretary'), ('Additonal Space','Additional Space'), ('storage','storage'), 
        ('assistant','assistant'), ('extra chair','extra chair'),
    ]
    PERIOD = [
        ('setup fee', 'setup fee'), ('one time fee', 'one time fee'), ('one time charge', 'one time charge'), ('hourly','hourly'), 
        ('daily','daily'), ('weekly','weekly'), ('monthly','monthly'), ('semi-annually', 'semi-annually'), ('annually','annually') 
    ]
    TERM = [('6 months', '6'), ('1 year', '1')] 
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    market_price_per_sq_ft = models.DecimalField(max_digits=20, decimal_places=2)
    price_per_sq_ft = models.DecimalField(max_digits=20, decimal_places=2)
    sq_ft = models.DecimalField(max_digits=20, decimal_places=2)
    rent = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    payment_period = models.CharField(max_length=17, choices=PERIOD)
    default_free_hours = models.PositiveIntegerField(default=4)
    free_hours = models.PositiveIntegerField(help_text="carry over hours")
    term_lease = models.PositiveIntegerField(help_text="number of payments") 
    lease_price_office = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    contract_file = models.FileField(upload_to='contracts/')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    sign_date = models.DateTimeField(auto_now_add=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    office_number = models.CharField(max_length=17, choices=OFFICE_CHOICES)
    type = models.CharField(max_length=10, choices=OFFICE_TYPE_CHOICES)
    is_available = models.BooleanField()
    access_card_number = models.ForeignKey('AccessCard', on_delete=models.CASCADE, related_name="access_card_office")
    amenity = models.CharField(max_length=200, choices=AMENITIES)
    scenario = models.CharField(max_length=30, choices=SCENARIOS)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate the total_price based on price and quantity
        self.rent = self.price_per_sq_ft * self.sq_ft - ( self.discount * 100 )
        self.lease_price_office = self.rent * self.term_lease

        super(Office, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.office_number} is rented until {self.end_date}"
    
class Virtual(models.Model):
    PACKAGE = [
        ('Gold', 'Gold'), ('Silver', 'Silver'), ('Bronze', 'Bronze')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.CharField(max_length=7, choices=PACKAGE)

    def __str__(self):
        return f"{self.user} is a {self.package} virtual customer"

class Company(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=200, null=True)
    street_number_company = models.CharField(max_length=20, null=True)
    street_name_company = models.CharField(max_length=200, null=True)
    city_company = models.CharField(max_length=100, null=True)   
    state_company = models.CharField(max_length=100, null=True)  
    zip_company = models.CharField(max_length=20, null=True)     
    address_company = models.CharField(max_length=200, null=True, blank=True)
    main_phone_company = models.CharField(max_length=20, null=True)
    home_phone_company = models.CharField(max_length=20, null=True)
    alt_phone_company = models.CharField(max_length=20, blank=True, null=True)
    alt_mobile_company = models.CharField(max_length=20, blank=True, null=True)
    alt_fax_company = models.CharField(max_length=20, blank=True, null=True)
    cell_company = models.CharField(max_length=20, blank=True, null=True)
    main_email_company = models.EmailField(max_length=40, null=True)
    cc_email_company = models.EmailField(max_length=40, blank=True, null=True)
    alt_email_1_company = models.EmailField(max_length=40, blank=True, null=True)
    alt_email_2_company = models.EmailField(max_length=40, blank=True, null=True)
    website_company = models.CharField(max_length=100, blank=True, null=True)
    other_1_company = models.CharField(max_length=50, blank=True, null=True)
    linkedin_company = models.CharField(max_length=100, blank=True, null=True)
    facebook_company = models.CharField(max_length=100, blank=True, null=True)
    x_company = models.CharField(max_length=100, blank=True, null=True)
    URL1_company = models.CharField(max_length=100, blank=True, null=True) 
    URL2_company = models.CharField(max_length=50, blank=True, null=True)
    URL3_company = models.CharField(max_length=50, blank=True, null=True)
    URL4_company = models.CharField(max_length=50, blank=True, null=True)
    skypeID_company = models.CharField(max_length=50, blank=True, null=True)
    other_2_company = models.CharField(max_length=50, blank=True, null=True)
    other_3_company = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    list_of_phone = models.CharField(max_length=1000, blank=True, null=True)
    list_of_email = models.CharField(max_length=1000, blank=True, null=True)
    logo = models.FileField(upload_to='logos/', blank=True, null=True)

    def save(self, *args, **kwargs):

        # Remove duplicates from phone and email lists
        phones = [
            phone.strip() for phone in [
                self.main_phone_company, 
                self.alt_phone_company, 
                self.alt_mobile_company, 
                self.home_phone_company, 
                self.cell_company
            ] if phone is not None and phone.strip()
        ]
        emails = [
            email.strip() for email in [
                self.alt_email_2_company, 
                self.alt_email_1_company, 
                self.cc_email_company, 
                self.main_email_company
            ] if email is not None and email.strip()
        ]

        # Remove duplicates by converting to a set and back to a list
        phones = list(set(phones))
        emails = list(set(emails))

        # Join the cleaned lists into 'list_of_phone' and 'list_of_email' fields
        self.list_of_phone = '\n'.join(phones)
        self.list_of_email = '\n'.join(emails)

        # Concatenate the four fields into the 'employee' field
        self.address_company = f"{self.street_number_company} {self.street_name_company}  " + \
            f"{self.city_company}, {self.state_company} {self.zip_company}"
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.company }\n - {self.address_company}"

class Owner(models.Model):
    NAME_PREFIX = [
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
        ('Dr.', 'Dr.'),
        ('Ms.', 'Ms.')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    name_prefix_owner = models.CharField(max_length=30, choices=NAME_PREFIX, null=True)
    last_name_owner = models.CharField(max_length=200, null=True)
    middle_name_owner = models.CharField(max_length=200, null=True)
    first_name_owner = models.CharField(max_length=200, null=True)
    owner = models.CharField(max_length=200, null=True, blank=True)
    street_number_owner = models.CharField(max_length=20, blank=True, null=True) 
    street_name_owner = models.CharField(max_length=200, blank=True, null=True) 
    city_owner = models.CharField(max_length=100, blank=True, null=True)    
    state_owner = models.CharField(max_length=100, blank=True, null=True)   
    zip_owner = models.CharField(max_length=20, blank=True, null=True)      
    home_address_owner = models.CharField(max_length=200, null=True, blank=True)
    main_phone_owner = models.CharField(max_length=20, blank=True, null=True)
    home_phone_owner = models.CharField(max_length=20, blank=True, null=True)
    alt_phone_owner = models.CharField(max_length=20, blank=True, null=True)
    alt_mobile_owner = models.CharField(max_length=20, blank=True, null=True)
    fax_owner = models.CharField(max_length=20, blank=True, null=True)
    cell_owner = models.CharField(max_length=20, blank=True, null=True)
    main_email_owner = models.EmailField(max_length=40, blank=True, null=True)
    cc_email_owner = models.EmailField(max_length=40, blank=True, null=True)
    alt_email_1_owner = models.EmailField(max_length=40, blank=True, null=True)
    alt_email_2_owner = models.EmailField(max_length=40, blank=True, null=True)
    website_owner = models.CharField(max_length=100, null=True, blank=True)
    other_1_owner = models.CharField(max_length=50, blank=True, null=True)
    linkedin_owner = models.CharField(max_length=100, blank=True, null=True)
    facebook_owner = models.CharField(max_length=100, blank=True, null=True)
    x_owner = models.CharField(max_length=100, blank=True, null=True)
    URL1_owner = models.CharField(max_length=100, blank=True, null=True) 
    URL2_owner = models.CharField(max_length=50, blank=True, null=True)
    URL3_owner = models.CharField(max_length=50, blank=True, null=True)
    URL4_owner = models.CharField(max_length=50, blank=True, null=True)
    skypeID_owner = models.CharField(max_length=50, blank=True, null=True)
    other_2_owner = models.CharField(max_length=50, blank=True, null=True)
    other_3_owner = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    list_of_phone = models.CharField(max_length=1000, blank=True, null=True)
    list_of_email = models.CharField(max_length=1000, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Remove duplicates from phone and email lists
        phones = [
            phone.strip() for phone in [
                self.main_phone_owner, 
                self.alt_phone_owner,
                self.alt_mobile_owner,
                self.home_phone_owner,
                self.cell_owner
            ] if phone is not None and phone.strip()
        ]
        emails = [
            email.strip() for email in [
                self.alt_email_2_owner,
                self.alt_email_1_owner, 
                self.cc_email_owner,
                self.main_email_owner
            ] if email is not None and email.strip()
        ]

        # Remove duplicates by converting to a set and back to a list
        phones = list(set(phones))
        emails = list(set(emails))

        # Join the cleaned lists into 'list_of_phone' and 'list_of_email' fields
        self.list_of_phone = '\n'.join(phones)
        self.list_of_email = '\n'.join(emails)

        # Concatenate the four fields into the 'employee' field
        self.owner = f"{self.name_prefix_owner} {self.first_name_owner} {self.middle_name_owner} {self.last_name_owner}"
        self.home_address_owner = f"{self.street_number_owner} {self.street_name_owner} {self.city_owner}, "\
            + f"{self.state_owner} {self.zip_owner}"
        super(Owner, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.owner } is our owner of record of {self.company}"

class Employee(models.Model):
    NAME_PREFIX = [
        ('Mr.', 'Mr.'),
        ('Mrs.', 'Mrs.'),
        ('Dr.', 'Dr.'),
        ('Ms.', 'Ms.')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    name_prefix_employee = models.CharField(max_length=30, choices=NAME_PREFIX, null=True)
    last_name_employee = models.CharField(max_length=200, null=True)
    middle_name_employee = models.CharField(max_length=200, null=True)
    first_name_employee = models.CharField(max_length=200, null=True)
    job_title_employee = models.CharField(max_length=200, null=True)
    employee = models.CharField(max_length=300, null=True, blank=True)
    street_number_employee = models.CharField(max_length=20, blank=True, null=True)     
    street_name_employee = models.CharField(max_length=200, blank=True, null=True)      
    city_employee = models.CharField(max_length=100, blank=True, null=True)             
    state_employee = models.CharField(max_length=100, blank=True, null=True)            
    zip_employee = models.CharField(max_length=20, blank=True, null=True)               
    address_employee = models.CharField(max_length=200, blank=True, null=True)
    main_phone_employee = models.CharField(max_length=20, blank=True, null=True)
    home_phone_employee = models.CharField(max_length=20, blank=True, null=True)
    alt_phone_employee = models.CharField(max_length=20, blank=True, null=True)
    alt_mobile_employee = models.CharField(max_length=20, blank=True, null=True)
    alt_fax_employee = models.CharField(max_length=20, blank=True, null=True)
    cell_employee = models.CharField(max_length=20, blank=True, null=True)
    main_email_employee = models.EmailField(max_length=40, blank=True, null=True)
    cc_email_employee = models.EmailField(max_length=40, blank=True, null=True)
    alt_email_1_employee = models.EmailField(max_length=40, blank=True, null=True)
    alt_email_2_employee = models.EmailField(max_length=40, blank=True, null=True)
    website_employee = models.CharField(max_length=100, blank=True, null=True)
    other_1_employee = models.CharField(max_length=50, blank=True, null=True)
    linkedin_employee = models.CharField(max_length=100, blank=True, null=True)
    facebook_employee = models.CharField(max_length=100, blank=True, null=True)
    x_employee = models.CharField(max_length=100, blank=True, null=True)
    URL1_employee = models.CharField(max_length=100, blank=True, null=True) 
    URL2_employee = models.CharField(max_length=50, blank=True, null=True)
    URL3_employee = models.CharField(max_length=50, blank=True, null=True)
    URL4_employee = models.CharField(max_length=50, blank=True, null=True)
    skypeID_employee = models.CharField(max_length=50, blank=True, null=True)
    other_2_employee = models.CharField(max_length=50, blank=True, null=True)
    other_3_employee = models.CharField(max_length=50, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    list_of_phone = models.CharField(max_length=1000, blank=True, null=True)
    list_of_email = models.CharField(max_length=1000, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Concatenate the four fields into the 'employee' field
        self.employee = f"{self.name_prefix_employee} {self.first_name_employee} {self.middle_name_employee} {self.last_name_employee}, {self.job_title_employee}"
        self.address_employee = f"{self.street_number_employee}{self.street_name_employee}{self.city_employee}, {self.state_employee} {self.zip_employee}"

        # Create lists for phones and emails
        phones = [phone.strip() for phone in [self.main_phone_employee, self.alt_phone_employee, self.alt_mobile_employee, self.home_phone_employee, self.cell_employee] if phone and phone.strip()]
        emails = [email.strip() for email in [self.alt_email_2_employee, self.alt_email_1_employee, self.cc_email_employee, self.main_email_employee] if email and email.strip()]

        # Remove duplicates by converting to a set and back to a list
        phones = list(set(phones))
        emails = list(set(emails))

        # Join the cleaned lists into 'list_of_phone' and 'list_of_email' fields
        self.list_of_phone = '\n'.join(phones)
        self.list_of_email = '\n'.join(emails)

        super(Employee, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee} of {self.company}"

class AccessCard(models.Model):
    ORDER_STATUS = [('processing', 'Processing'), ('completed', 'Completed'), ('shipped', 'Shipped'), ('Received', 'Received')]
    CARD_NUMBER = [('A446F45k556', 'A446F45k556'), ('A44gG45k556', 'A44gG45k556'), ('A446F77k556', 'A446F77k556'), ('A446F45fg56', 'A446F45fg56'), ('A446Fhhh556', 'A446Fhhh556')]
    CODE = [('happy', 'Happy'), ('truth', 'Truth'), ('smile', 'Smile'), ('good', 'Good'), ('enjoy', 'Enjoy')]
    REFERENCE = [('OR#F45k556', 'OR#F45k556'), ('OR#gG45k556', 'OR#gG45k556'), ('OR#F77k556', 'OR#F77k556'), ('OR#F45fg56', 'OR#F45fg56'), ('OR#Fhhh556', 'OR#Fhhh556')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, default="60.00")
    payment_received = models.BooleanField(default=False)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS)
    card_number = models.CharField(max_length=20, blank=True, null=True, unique=True, choices=CARD_NUMBER)
    comments = models.TextField(blank=True, null=True)
    discount_code = models.CharField(max_length=20, blank=True, null=True, choices=CODE)
    order_reference = models.CharField(max_length=50, unique=True, choices=REFERENCE)
    quantity = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="will automatically fill based on quantity no matter what value is here")

    def save(self, *args, **kwargs):
        # Calculate the total_price based on price and quantity
        self.total_price = self.price * self.quantity

        super(AccessCard, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} Access Card(s), Card No: {self.card_number}, issued to {self.employee} at a total price of {self.total_price}"
    
    def total_cost(self):
        return self.price * self.quantity
    

class Client(models.Model):
    DEFAULT_HOURLY_RATE = [('35', '$35.00')]
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=100)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE) # good idea if theres multiple owners
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    virtual = models.ForeignKey(Virtual, on_delete=models.CASCADE, related_name="virtual_package")
    list_of_phone = models.CharField(max_length=1000, blank=True, null=True)
    list_of_email = models.CharField(max_length=1000, blank=True, null=True)

    def save(self, *args, **kwargs):

        phones = [
            phone.strip() for phone in '\n'.join([
                self.company.list_of_phone,
                self.employee.list_of_phone,
                self.owner.list_of_phone
            ]).split('\n') if phone.strip()
        ]
        emails = [
            email.strip() for email in '\n'.join([
                self.employee.list_of_email, 
                self.owner.list_of_email, 
                self.company.list_of_email
            ]).split('\n') if email.strip()
        ]

        # Remove duplicates by converting to a set and back to a list
        phones = list(set(phones))
        emails = list(set(emails))

        # Join the cleaned lists into 'list_of_phone' and 'list_of_email' fields
        self.list_of_phone = '\n'.join(phones)
        self.list_of_email = '\n'.join(emails)

        super(Client, self).save(*args, **kwargs)

    def __str__(self):
        return f"name: {self.name} employee: {self.employee} owner: {self.owner} company: {self.company}"


class Building(models.Model):
    BUILDINGS = [
        ('West Boca Executive Suites', 'West Boca Executive Suites'),
        ('7777 Glade Road', '7777 Glade Road'),
    ]
    name = models.CharField(max_length=500)
    address = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.name} - {self.address}"


class ConferenceRoom(models.Model):
    CONFERENCE_ROOMS = [
        ('Main Conference Room', 'Main Conference Room'),
        ('North Conference Room', 'North Conference Room'),
        ('Put Your Conference Room Name Here', 'Put Your Conference Room Name Here')
    ]
    name = models.CharField(max_length=50)
    building = models.ManyToManyField(Building)
    max_capacity = models.PositiveIntegerField(default=12)
    seating_capacity = models.PositiveIntegerField(default=10)
    
    # Other room-related field
    def __str__(self):
        return f"{self.name} with max capacity of {self.max_capacity} and seating capacity of {self.seating_capacity}"

class Booking(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    room = models.ForeignKey(ConferenceRoom, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    duration_hours = models.PositiveIntegerField(default=1)
    confirmation = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.end_datetime:
            self.end_datetime = self.start_datetime + timedelta(hours=self.duration_hours)
        else:
            difference = self.end_datetime - self.start_datetime
            hours_from_days = difference.days * 24
            hours_from_seconds = difference.seconds//3600
            self.duration_hours = hours_from_days + hours_from_seconds
            
        # Generate a "mashup" confirmation number
        # name_slug = slugify(self.client.name)
        # room_slug = slugify(self.room.room)
        # start_time_slug = self.start_time.strftime('%Y%m%d%H%M')
        # self.confirmation = f"{name_slug}-{room_slug}-{start_time_slug}"
        datetime_format = "%Y%m%d%H"
        formatted_datetimes = self.start_datetime.strftime(datetime_format)+self.end_datetime.strftime(datetime_format)
        self.confirmation = f"{self.room.pk:05d}{formatted_datetimes}"
        
        super(Booking, self).save(*args, **kwargs)

    def clean(self):
        # Ensure that start_time only contains the hour with zero minutes and zero seconds
        if self.start_datetime.minute != 0 or self.start_datetime.second != 0:
            raise ValidationError('Start time should only have the hour with zero minutes and zero seconds.')

    def __str__(self):
        return f"{self.client.name} has scheduled the {self.room} in between {self.start_datetime} and {self.end_datetime}"
    
    
class HangingLicense(models.Model):
    name = models.CharField(max_length=120)

# class AdditionalCompany(models.Model):
#     

# class Receptionist(models.Model):
#     

# class Address(models.Model):
#     

# class PhoneNumber(models.Model):
#     

# class Phone(models.Model):
#     

# class Fax(models.Model):
#     

# class Projector(models.Model):
#     

# class Scanner(models.Model):
#     

# class Chair(models.Model):
#     

# class RefreshmentsService(models.Model):
#     

# class CableTV(models.Model):
#     

# class EngravedDirectorySign(models.Model):
#     

# class EngravedMailSign(models.Model):
#     

# class Keys(models.Model):
#     

# class LeaseAgreement(models.Model):
#     
    
# class RentalService(models.Model):
#     

# class Billing(models.Model):
#     

# class Reports(models.Model):
#     

