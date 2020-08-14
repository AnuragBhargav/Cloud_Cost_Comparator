**Create Table in AWS:**

create table instances (date DATETIME, type_m VARCHAR(250),memory_in VARCHAR(250),vcpu SMALLINT,machine_type VARCHAR(255),region VARCHAR(255), cost_per_hr FLOAT(10,4));

**Create Table in GCP:**

create table instances (date DATETIME, machine_type VARCHAR(255),region VARCHAR(255), memory_in SMALLINT,vcpu SMALLINT, cost_per_hr FLOAT(10,4));