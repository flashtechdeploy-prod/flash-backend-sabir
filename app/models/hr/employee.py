"""Employee model - unified employee records."""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Employee(Base):
    """Unified Employee model combining all employee fields."""
    
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Primary identifiers
    employee_id = Column(String(100), unique=True, index=True, nullable=True)
    serial_no = Column(String(100), index=True)  # FSS serial number
    fss_no = Column(String(100), index=True)  # FSS number
    
    # Basic info
    first_name = Column(Text)
    last_name = Column(Text)
    name = Column(Text)  # Combined name field (for compatibility)
    father_name = Column(Text)
    gender = Column(Text)
    date_of_birth = Column(Text)
    dob = Column(Text)  # Alternative DOB field
    
    # Rank and status
    rank = Column(Text)
    rank2 = Column(Text)
    status = Column(Text)  # Army/Civil/PAF etc
    status2 = Column(Text)
    unit = Column(Text)
    unit2 = Column(Text)
    category = Column(Text)  # Office Staff, Operational Staff, etc.
    
    # Profile and photos
    profile_photo = Column(Text)
    avatar_url = Column(Text)
    
    # Government IDs
    government_id = Column(Text)
    cnic = Column(Text, index=True)
    cnic_expiry_date = Column(Text)
    cnic_expiry = Column(Text)  # Alternative field
    
    # Documents
    domicile = Column(Text)
    documents_held = Column(Text)
    original_doc_held = Column(Text)
    documents_handed_over_to = Column(Text)
    photo_on_document = Column(Text)
    photo_on_doc = Column(Text)
    orig_docs_received = Column(Text)
    
    # Languages
    languages_spoken = Column(Text)  # JSON array string
    languages_proficiency = Column(Text)  # JSON array
    
    # Physical attributes
    height_cm = Column(Integer)
    height = Column(Text)
    blood_group = Column(Text)
    
    # Contact info
    email = Column(String(100), unique=True, index=True, nullable=True)
    mobile_number = Column(Text)
    mobile_no = Column(Text)
    personal_phone_number = Column(Text)
    home_contact_no = Column(Text)
    home_contact = Column(Text)
    emergency_contact_name = Column(Text)
    emergency_contact_number = Column(Text)
    
    # Family
    next_of_kin_name = Column(Text)
    next_of_kin_cnic = Column(Text)
    next_of_kin_mobile_number = Column(Text)
    nok_name = Column(Text)
    nok_relationship = Column(Text)
    sons_names = Column(Text)
    daughters_names = Column(Text)
    brothers_names = Column(Text)
    sisters_names = Column(Text)
    sons_count = Column(Text)
    daughters_count = Column(Text)
    brothers_count = Column(Text)
    sisters_count = Column(Text)
    
    # Permanent address
    permanent_address = Column(Text)
    permanent_village = Column(Text)
    permanent_post_office = Column(Text)
    permanent_thana = Column(Text)
    permanent_tehsil = Column(Text)
    permanent_district = Column(Text)
    village = Column(Text)
    post_office = Column(Text)
    thana = Column(Text)
    tehsil = Column(Text)
    district = Column(Text)
    address_details = Column(Text)
    
    # Present/Temporary address
    temporary_address = Column(Text)
    present_village = Column(Text)
    present_post_office = Column(Text)
    present_thana = Column(Text)
    present_tehsil = Column(Text)
    present_district = Column(Text)
    temp_village = Column(Text)
    temp_post_office = Column(Text)
    temp_thana = Column(Text)
    temp_tehsil = Column(Text)
    temp_district = Column(Text)
    temp_city = Column(Text)
    temp_phone = Column(Text)
    temp_address_details = Column(Text)
    
    # Location
    city = Column(Text)
    state = Column(Text)
    postal_code = Column(Text)
    duty_location = Column(Text)
    base_location = Column(Text)
    last_site_assigned = Column(Text)
    
    # Employment details
    department = Column(Text)
    designation = Column(Text)
    enrolled_as = Column(Text)
    employment_type = Column(Text)
    shift_type = Column(Text)
    reporting_manager = Column(Text)
    interviewed_by = Column(Text)
    introduced_by = Column(Text)
    employment_status = Column(Text, default="Active")
    allocation_status = Column(Text, default="Free")  # Free / Allocated
    previous_employment = Column(Text)
    
    # Security and training
    security_clearance = Column(Text)
    basic_security_training = Column(Boolean, default=False)
    fire_safety_training = Column(Boolean, default=False)
    first_aid_certification = Column(Boolean, default=False)
    agreement = Column(Boolean, default=False)
    police_clearance = Column(Boolean, default=False)
    fingerprint_check = Column(Boolean, default=False)
    background_screening = Column(Boolean, default=False)
    reference_verification = Column(Boolean, default=False)
    guard_card = Column(Boolean, default=False)
    
    # Document files
    guard_card_doc = Column(Text)
    police_clearance_doc = Column(Text)
    fingerprint_check_doc = Column(Text)
    background_screening_doc = Column(Text)
    reference_verification_doc = Column(Text)
    other_certificates = Column(Text)  # JSON string
    
    # Document attachments (URLs)
    cnic_attachment = Column(Text)
    domicile_attachment = Column(Text)
    sho_verified_attachment = Column(Text)
    ssp_verified_attachment = Column(Text)
    khidmat_verified_attachment = Column(Text)
    police_trg_attachment = Column(Text)
    photo_on_doc_attachment = Column(Text)
    personal_signature_attachment = Column(Text)
    recording_officer_signature_attachment = Column(Text)
    fingerprint_thumb_attachment = Column(Text)
    fingerprint_index_attachment = Column(Text)
    fingerprint_middle_attachment = Column(Text)
    fingerprint_ring_attachment = Column(Text)
    fingerprint_pinky_attachment = Column(Text)
    employment_agreement_attachment = Column(Text)
    served_in_attachment = Column(Text)
    vaccination_attachment = Column(Text)
    experience_security_attachment = Column(Text)
    education_attachment = Column(Text)
    nok_cnic_attachment = Column(Text)
    other_documents_attachment = Column(Text)
    
    # Salary and banking
    salary = Column(Text)
    basic_salary = Column(Text)
    allowances = Column(Text)
    total_salary = Column(Text)
    bank_name = Column(Text)
    account_number = Column(Text)
    ifsc_code = Column(Text)
    account_type = Column(Text)
    tax_id = Column(Text)
    bank_accounts = Column(Text)  # JSON array string
    payments = Column(Text)
    
    # Benefits
    eobi_no = Column(Text)
    insurance = Column(Text)
    social_security = Column(Text)
    
    # System access
    system_access_rights = Column(Text)
    
    # Service history
    retired_from = Column(Text)  # JSON array string
    served_in = Column(Text)
    service_unit = Column(Text)
    service_rank = Column(Text)
    service_enrollment_date = Column(Text)
    service_reenrollment_date = Column(Text)
    enrolled = Column(Text)
    re_enrolled = Column(Text)
    experience_security = Column(Text)
    deployment_details = Column(Text)
    
    # Medical
    medical_category = Column(Text)
    medical_details = Column(Text)
    medical_discharge_cause = Column(Text)
    discharge_cause = Column(Text)
    dod = Column(Text)  # Date of Discharge
    
    # Education
    civil_education_type = Column(Text)
    civil_education_detail = Column(Text)
    education = Column(Text)
    
    # Verification
    particulars_verified_by_sho_on = Column(Text)
    particulars_verified_by_ssp_on = Column(Text)
    police_khidmat_verification_on = Column(Text)
    verified_by_khidmat_markaz = Column(Text)
    verified_by_sho = Column(Text)
    verified_by_ssp = Column(Text)
    police_training_letter_date = Column(Text)
    police_trg_ltr_date = Column(Text)
    
    # Signatures
    signature_recording_officer = Column(Text)
    signature_individual = Column(Text)
    fingerprint_attested_by = Column(Text)
    
    # FSS specific
    fss_number = Column(Text)
    fss_name = Column(Text)
    fss_so = Column(Text)
    vol_no = Column(Text)
    volume_no = Column(Text)
    
    # Vaccination
    vaccination_certificate = Column(Text)
    vaccination_cert = Column(Text)
    
    # Card and entry
    date_of_entry = Column(Text)
    card_number = Column(Text)
    
    # Remarks
    remarks = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Employee {self.id} - {self.name or f'{self.first_name} {self.last_name}'}>"
