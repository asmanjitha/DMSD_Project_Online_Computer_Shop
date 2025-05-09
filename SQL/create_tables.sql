
DROP TABLE IF EXISTS TransactionDetails, SalesTransaction, ShoppingBasket, SpecialOffer, ShippingAddress, CreditCard, Customer, Product, ProductType;

-- Customers
CREATE TABLE Customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    home_address TEXT,
    status ENUM('regular', 'silver', 'gold', 'platinum') DEFAULT 'regular',
    credit_amount DECIMAL(10, 2)
);

--Admins
CREATE TABLE Admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(100) NOT NULL
);

-- Credit Cards
CREATE TABLE CreditCard (
    card_number VARCHAR(20) PRIMARY KEY,
    customer_id INT,
    security_code VARCHAR(5),
    owner_name VARCHAR(100),
    billing_address TEXT,
    card_type VARCHAR(20),
    expiry_date DATE,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE
);

-- Shipping Addresses
CREATE TABLE ShippingAddress (
    customer_id INT,
    address_name VARCHAR(50),
    zip_code VARCHAR(10),
    street_name VARCHAR(100),
    street_number VARCHAR(20),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    PRIMARY KEY (customer_id, address_name),
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id) ON DELETE CASCADE
);

-- Product Types
CREATE TABLE ProductType (
    type_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    category ENUM('desktop', 'laptop', 'printer', 'other'),
    cpu_type VARCHAR(50),
    weight DECIMAL(5,2),
    battery_life INT,
    resolution VARCHAR(50),
    printer_type VARCHAR(50)
);

-- Products
CREATE TABLE Product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    recommended_price DECIMAL(10,2),
    quantity_in_stock INT,
    type_id INT,
    FOREIGN KEY (type_id) REFERENCES ProductType(type_id)
);

-- Special Offers (for gold and platinum customers)
CREATE TABLE SpecialOffer (
    offer_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    offer_price DECIMAL(10,2),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);


-- Shopping Cart Item
CREATE TABLE ShoppingCartItem (
    cart_item_id INT AUTO_INCREMENT PRIMARY KEY,
    basket_id INT,
    product_id INT,
    quantity INT DEFAULT 1,
    FOREIGN KEY (basket_id) REFERENCES ShoppingBasket(basket_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);


-- Shopping Basket (temporary before finalizing a sale)
CREATE TABLE ShoppingBasket (
    basket_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
);

-- Sales Transactions
CREATE TABLE SalesTransaction (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    basket_id INT,
    card_number VARCHAR(20),
    shipping_customer_id INT,
    shipping_address_name VARCHAR(50),
    total_amount DECIMAL(10,2),
    status ENUM('confirmed', 'not-delivered') DEFAULT 'confirmed',
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (basket_id) REFERENCES ShoppingBasket(basket_id),
    FOREIGN KEY (card_number) REFERENCES CreditCard(card_number),
    FOREIGN KEY (shipping_customer_id, shipping_address_name)
        REFERENCES ShippingAddress(customer_id, address_name)
);

-- Transaction Details (products bought in a transaction)
CREATE TABLE TransactionDetails (
    transaction_id INT,
    product_id INT,
    quantity INT,
    final_price DECIMAL(10,2),
    PRIMARY KEY (transaction_id, product_id),
    FOREIGN KEY (transaction_id) REFERENCES SalesTransaction(transaction_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id)
);

-- Customer Tiers
CREATE TABLE Tier (
    tier_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);
