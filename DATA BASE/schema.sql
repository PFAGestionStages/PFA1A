CREATE TYPE user_role AS ENUM ('student', 'company', 'school', 'admin');
CREATE TYPE application_status AS ENUM (
'submitted',
'under_company_review',
'accepted_by_company',
'rejected_by_company',
'pending_school_approval',
'approved_by_school',
'rejected_by_school',
'internship_started',
'internship_completed'
);
CREATE TYPE offer_status AS ENUM ('draft', 'published', 'closed')

CREATE TABLE users (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
first_name VARCHAR(100) NOT NULL,
last_name VARCHAR(100) NOT NULL,
email VARCHAR(255) UNIQUE NOT NULL,
password_hash TEXT NOT NULL,
role user_role NOT NULL,
phone VARCHAR(30),
profile_picture TEXT,
is_active BOOLEAN DEFAULT TRUE,
last_login TIMESTAMP,
created_at TIMESTAMP DEFAULT NOW(),
updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE schools (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,
school_name VARCHAR(255) NOT NULL,
acronym VARCHAR(50),
website TEXT,
address TEXT,
approval_workflow_enabled BOOLEAN DEFAULT TRUE
);


CREATE TABLE students (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
school_id UUID REFERENCES schools(id),
student_code VARCHAR(50),
program VARCHAR(255),
level VARCHAR(50),
graduation_year INTEGER,
bio TEXT,
cv_file_id UUID REFERENCES files(id),
linkedin_url TEXT,
github_url TEXT,
portfolio_url TEXT,
profile_completion INTEGER DEFAULT 0
);

CREATE TABLE companies (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
company_name VARCHAR(255) NOT NULL,
industry VARCHAR(255),
description TEXT,
website TEXT,
logo_url TEXT,
size VARCHAR(50),
city VARCHAR(100),
country VARCHAR(100),
contact_person VARCHAR(255),
is_verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE files (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
original_name TEXT NOT NULL,
stored_name TEXT NOT NULL,
path TEXT NOT NULL,
mime_type VARCHAR(100),
size_bytes BIGINT,
uploaded_by UUID REFERENCES users(id),
uploaded_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE skills (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
name VARCHAR(100) UNIQUE NOT NULL,
category VARCHAR(100)
);

CREATE TABLE student_skills (
student_id UUID REFERENCES students(id) ON DELETE CASCADE,
skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
level INTEGER,
PRIMARY KEY (student_id, skill_id)
);

CREATE TABLE internship_offers (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
title VARCHAR(255) NOT NULL,
description TEXT,
requirements TEXT,
responsibilities TEXT,
location VARCHAR(255),
internship_type VARCHAR(100),
duration_months INTEGER,
start_date DATE,
end_date DATE,
compensation NUMERIC(10,2),
remote_allowed BOOLEAN DEFAULT FALSE,
slots_available INTEGER DEFAULT 1,
status offer_status DEFAULT 'draft',
is_active BOOLEAN DEFAULT TRUE,
published_at TIMESTAMP,
created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE offer_skills (
offer_id UUID REFERENCES internship_offers(id) ON DELETE CASCADE,
skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
required_level INTEGER,
PRIMARY KEY (offer_id, skill_id)
);

CREATE TABLE applications (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
offer_id UUID NOT NULL REFERENCES internship_offers(id) ON DELETE CASCADE,
cover_letter TEXT,
status application_status DEFAULT 'submitted',
applied_at TIMESTAMP DEFAULT NOW(),
company_reviewed_at TIMESTAMP,
school_reviewed_at TIMESTAMP,
final_decision_at TIMESTAMP,
UNIQUE(student_id, offer_id)
);

CREATE TABLE application_status_history (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
application_id UUID REFERENCES applications(id) ON DELETE CASCADE,
old_status application_status,
new_status application_status,
changed_by UUID REFERENCES users(id),
comment TEXT,
changed_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE application_documents (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
application_id UUID REFERENCES applications(id) ON DELETE CASCADE,
file_id UUID REFERENCES files(id) ON DELETE CASCADE,
document_type VARCHAR(50) NOT NULL
);

CREATE TABLE internship_agreements (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
application_id UUID UNIQUE REFERENCES applications(id) ON DELETE CASCADE,
agreement_number VARCHAR(100) UNIQUE,
generated_at TIMESTAMP,
signed_by_student BOOLEAN DEFAULT FALSE,
signed_by_company BOOLEAN DEFAULT FALSE,
signed_by_school BOOLEAN DEFAULT FALSE,
final_pdf_file_id UUID REFERENCES files(id)
);

CREATE TABLE notifications (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
user_id UUID REFERENCES users(id) ON DELETE CASCADE,
title VARCHAR(255) NOT NULL,
message TEXT,
type VARCHAR(50),
is_read BOOLEAN DEFAULT FALSE,
created_at TIMESTAMP DEFAULT NOW()
);