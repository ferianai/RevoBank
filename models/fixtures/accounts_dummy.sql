INSERT INTO accounts (
    user_id, account_type, account_number, balance, image_uri, name, birth_date,
    address, gender, phone, created_at, updated_at
)
VALUES
-- Account untuk john_doe (user_id = 1)
(1, 'SAVINGS', 'ACC1234567890', 15000.00, NULL, 'John Doe', '1990-05-20',
 '123 Main Street', 'Male', '081234567890', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Account untuk jane_smith (user_id = 2)
(2, 'CURRENT', 'ACC9876543210', 52000.00, NULL, 'Jane Smith', '1985-11-10',
 '456 Second Avenue', 'Female', '081298765432', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Account untuk bob_johnson (user_id = 3)
(3, 'SAVINGS', 'ACC1112223334', 8800.50, NULL, 'Bob Johnson', '1992-08-15',
 '789 Third Blvd', 'Male', '082345678912', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Account untuk alice_wonder (user_id = 4)
(4, 'SAVINGS', 'ACC5556667778', 0.00, NULL, 'Alice Wonder', '1995-02-28',
 'Wonderland Street 1', 'Female', '083212341234', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Account untuk admin_user (user_id = 5)
(5, 'ADMIN', 'ACC9998887776', 1000000.00, NULL, 'Admin User', '1980-01-01',
 'Admin HQ', 'Other', '089912345678', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

    -- id: int = db.Column(db.Integer, primary_key=True)
    -- user_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    -- account_type: str = db.Column(db.String(100), nullable=False)  # Increased length
    -- account_number: str = db.Column(
    --     db.String(40), unique=True, nullable=False
    -- )  # Increased length
    -- balance: float = db.Column(db.Numeric(10, 2), default=0.00)
    -- image_uri: str = db.Column(db.Text)
    -- name: str = db.Column(db.String(100), nullable=False)
    -- birth_date: datetime = db.Column(db.Date)
    -- address: str = db.Column(db.String(255))
    -- gender: str = db.Column(db.String(20))  # Increased length
    -- phone: str = db.Column(db.String(300))  # Increased length
    -- created_at: datetime = db.Column(db.DateTime, default=crono.now)
    -- updated_at: datetime = db.Column(db.DateTime, default=crono.now, onupdate=crono.now)