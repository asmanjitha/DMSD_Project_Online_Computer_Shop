-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 09, 2025 at 02:41 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `newarkit_dev`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `username`, `password`) VALUES
(1, 'asm277@njit.edu', '123'),
(3, 'asmanjitha@gmail.com', '123'),
(4, 'admin@newark.com', 'admin'),
(5, 'vamsikushal@gmail.com', 'vipgentleman');

-- --------------------------------------------------------

--
-- Table structure for table `creditcard`
--

CREATE TABLE `creditcard` (
  `card_number` varchar(20) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `security_code` varchar(5) DEFAULT NULL,
  `owner_name` varchar(100) DEFAULT NULL,
  `billing_address` text DEFAULT NULL,
  `card_type` varchar(20) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `creditcard`
--

INSERT INTO `creditcard` (`card_number`, `customer_id`, `security_code`, `owner_name`, `billing_address`, `card_type`, `expiry_date`) VALUES
('11112222', 9, '090', 'CS631', 'cjhfelj', 'Visa', '2025-05-31'),
('1233456765486575', 9, '090', 'CS631', 'hkgrjvrlvhjkjgv', 'Visa', '2025-05-31'),
('123445567889', 5, '123', 'asm', '351 ELM ST\r\nApartment 2', 'visa', '2025-05-31'),
('1234567890', 2, '000', 'Akhitha', '351 ELM ST\r\nApartment 2', 'Master', '2027-10-28');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `customer_id` int(11) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `home_address` text DEFAULT NULL,
  `status` enum('regular','silver','gold','platinum') DEFAULT 'regular',
  `credit_amount` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`customer_id`, `first_name`, `last_name`, `email`, `password`, `phone`, `home_address`, `status`, `credit_amount`) VALUES
(2, 'Akhitha', 'Manjitha', 'asm277@njit.edu', '', '8625886354', '351 ELM ST\r\nApartment 2', 'regular', NULL),
(4, 'Senith', 'Senith', 'asm@gmail.com', 'scrypt:32768:8:1$kw2IHX6UhUEz5K6i$a5e3503ba0b049d9caf9c04f484981382cab950a088546fac49c10673f0f27ee55d8d6cd39912190bfdbea7ee539b4ba0c38f173cbe49d4bc7f57534c753389c', NULL, NULL, 'silver', NULL),
(5, 'Senith', 'Manjitha', 'asmanjitha@gmail.com', 'scrypt:32768:8:1$qKSlSnmwX8Kajtc7$be93ca9ae38abc3bcd0d017209f75482a0f7a08b5fbc12618f60e8049519f3a7c30df00874b511482d5749a5ecc1d049e7c3a79090374866ebd445f91362ef81', NULL, NULL, 'gold', NULL),
(6, 'User', 'User', 'user@newark.com', 'scrypt:32768:8:1$3RrG6xMuZ8RGv4Po$6ebbb939c5b841eeeccd8c94747770b34648f93622ddd957e306d26279b209ebc26f46f0828f8c2fda74e5433dc527e37ca936a07a064fa6632dbaf732a50b71', NULL, NULL, 'platinum', NULL),
(7, 'kushal', 'srinivas', 'kushalsrinivas@gmail.com', 'scrypt:32768:8:1$zWNw4M2SeaXWbwYJ$826a5a29f2a0235de8eddf1c20d863d61b18c28e0376736547683d04a904c7bf9cd634373303ed0c64751ba5a47f1b1fcc621f409dea83eb955f98bf2bff8270', NULL, NULL, 'regular', NULL),
(8, 'kushal', 'srinivas', 'kushalsrinivas73@gmail.com', 'scrypt:32768:8:1$Jk6tb2M7F4tJrmwZ$f742083e2ace53b966d76bef26b341d8ae91aafed0a839b82901a436838d8a812e2b4c88290b4980f6e921cbeb1e3c000301175cc26ff5c373b063f4c1fcf272', NULL, NULL, 'regular', NULL),
(9, 'CS631', '002', 'CS631@gmail.com', 'scrypt:32768:8:1$YCwd8SFIUUipYV2O$84e5eda7834f43ebe08b59e0027b344d32a39fea06865c771d614f822e4c10dd5d209639627209e2f653a420adb57368a8e9cee15eb3683027b932ba2d6854a1', NULL, NULL, 'regular', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `product_id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `recommended_price` decimal(10,2) DEFAULT NULL,
  `quantity_in_stock` int(11) DEFAULT NULL,
  `type_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`product_id`, `name`, `description`, `recommended_price`, `quantity_in_stock`, `type_id`) VALUES
(3, 'Dell Laptop', 'Intel CPu', 600.00, 10, 1),
(4, 'Dell printer', 'Dell printer', 100.00, 5, 2),
(7, 'MS Laptop', 'cdopvkmv', 200.00, 4, 4),
(8, 'HP Desktop', 'cfjnclifirfnvcfr', 1000.00, 200, 5);

-- --------------------------------------------------------

--
-- Table structure for table `producttype`
--

CREATE TABLE `producttype` (
  `type_id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `category` enum('desktop','laptop','printer','other') DEFAULT NULL,
  `cpu_type` varchar(50) DEFAULT NULL,
  `weight` decimal(5,2) DEFAULT NULL,
  `battery_life` int(11) DEFAULT NULL,
  `resolution` varchar(50) DEFAULT NULL,
  `printer_type` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `producttype`
--

INSERT INTO `producttype` (`type_id`, `name`, `category`, `cpu_type`, `weight`, `battery_life`, `resolution`, `printer_type`) VALUES
(1, 'Dell', 'laptop', 'Intel', 2.00, 4, '2k', ''),
(2, 'Dell Printer', 'printer', '', 0.00, 0, '', 'Laser'),
(3, 'Asus Laptop', 'laptop', 'Intel', 2.00, 20, '', ''),
(4, 'MS Laptop', 'laptop', 'Intel', 2.00, 12, '', ''),
(5, 'HP Desktop', 'desktop', 'AMD', 2.00, 0, '', '');

-- --------------------------------------------------------

--
-- Table structure for table `salestransaction`
--

CREATE TABLE `salestransaction` (
  `transaction_id` int(11) NOT NULL,
  `basket_id` int(11) DEFAULT NULL,
  `card_number` varchar(20) DEFAULT NULL,
  `shipping_customer_id` int(11) DEFAULT NULL,
  `shipping_address_name` varchar(50) DEFAULT NULL,
  `total_amount` decimal(10,2) DEFAULT NULL,
  `status` enum('confirmed','not-delivered') DEFAULT 'confirmed',
  `transaction_date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `salestransaction`
--

INSERT INTO `salestransaction` (`transaction_id`, `basket_id`, `card_number`, `shipping_customer_id`, `shipping_address_name`, `total_amount`, `status`, `transaction_date`) VALUES
(2, 2, '1234567890', 2, 'My Home', 600.00, 'not-delivered', '2025-04-28 17:16:56'),
(3, 3, '123445567889', 5, 'my home', 100.00, 'not-delivered', '2025-05-07 23:05:47'),
(4, 6, '1233456765486575', 9, 'Home', 0.00, 'confirmed', '2025-05-08 13:51:22'),
(5, 6, '1233456765486575', 9, 'Home', 1000.00, 'confirmed', '2025-05-08 13:53:24'),
(6, 6, '11112222', 9, 'Home', 100.00, 'confirmed', '2025-05-08 13:56:37');

-- --------------------------------------------------------

--
-- Table structure for table `shippingaddress`
--

CREATE TABLE `shippingaddress` (
  `customer_id` int(11) NOT NULL,
  `address_name` varchar(50) NOT NULL,
  `zip_code` varchar(10) DEFAULT NULL,
  `street_name` varchar(100) DEFAULT NULL,
  `street_number` varchar(20) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shippingaddress`
--

INSERT INTO `shippingaddress` (`customer_id`, `address_name`, `zip_code`, `street_name`, `street_number`, `city`, `state`, `country`) VALUES
(2, 'My Home', '07032', 'Elm Street', '351', 'Kearny', 'NJ', 'United States'),
(5, 'my home', '07032', 'Elm Street ', '351 ', 'Kearny', 'NJ', 'USA'),
(9, 'Home', '07032', 'elM ST', '34', 'harrison', 'NJ', 'USA');

-- --------------------------------------------------------

--
-- Table structure for table `shoppingbasket`
--

CREATE TABLE `shoppingbasket` (
  `basket_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shoppingbasket`
--

INSERT INTO `shoppingbasket` (`basket_id`, `customer_id`, `created_at`) VALUES
(2, 2, '2025-04-28 16:48:59'),
(3, 5, '2025-05-07 22:19:58'),
(4, 6, '2025-05-08 00:11:27'),
(5, 8, '2025-05-08 12:16:44'),
(6, 9, '2025-05-08 13:49:42');

-- --------------------------------------------------------

--
-- Table structure for table `shoppingcartitem`
--

CREATE TABLE `shoppingcartitem` (
  `cart_item_id` int(11) NOT NULL,
  `basket_id` int(11) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  `quantity` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `shoppingcartitem`
--

INSERT INTO `shoppingcartitem` (`cart_item_id`, `basket_id`, `product_id`, `quantity`) VALUES
(17, 3, 3, 1),
(18, 4, 3, 1),
(19, 5, 3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `specialoffer`
--

CREATE TABLE `specialoffer` (
  `offer_id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `offer_price` decimal(10,2) DEFAULT NULL,
  `allowed_status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `specialoffer`
--

INSERT INTO `specialoffer` (`offer_id`, `product_id`, `offer_price`, `allowed_status`) VALUES
(1, 3, 100.00, 'gold'),
(2, 4, 10.00, 'platinum');

-- --------------------------------------------------------

--
-- Table structure for table `transactiondetails`
--

CREATE TABLE `transactiondetails` (
  `transaction_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `final_price` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactiondetails`
--

INSERT INTO `transactiondetails` (`transaction_id`, `product_id`, `quantity`, `final_price`) VALUES
(2, 3, 1, 500.00),
(2, 4, 1, 100.00),
(3, 4, 1, 100.00),
(5, 8, 1, 1000.00),
(6, 4, 1, 100.00);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `creditcard`
--
ALTER TABLE `creditcard`
  ADD PRIMARY KEY (`card_number`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`product_id`),
  ADD KEY `type_id` (`type_id`);

--
-- Indexes for table `producttype`
--
ALTER TABLE `producttype`
  ADD PRIMARY KEY (`type_id`);

--
-- Indexes for table `salestransaction`
--
ALTER TABLE `salestransaction`
  ADD PRIMARY KEY (`transaction_id`),
  ADD KEY `basket_id` (`basket_id`),
  ADD KEY `card_number` (`card_number`),
  ADD KEY `shipping_customer_id` (`shipping_customer_id`,`shipping_address_name`);

--
-- Indexes for table `shippingaddress`
--
ALTER TABLE `shippingaddress`
  ADD PRIMARY KEY (`customer_id`,`address_name`);

--
-- Indexes for table `shoppingbasket`
--
ALTER TABLE `shoppingbasket`
  ADD PRIMARY KEY (`basket_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `shoppingcartitem`
--
ALTER TABLE `shoppingcartitem`
  ADD PRIMARY KEY (`cart_item_id`),
  ADD KEY `basket_id` (`basket_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `specialoffer`
--
ALTER TABLE `specialoffer`
  ADD PRIMARY KEY (`offer_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `transactiondetails`
--
ALTER TABLE `transactiondetails`
  ADD PRIMARY KEY (`transaction_id`,`product_id`),
  ADD KEY `product_id` (`product_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `producttype`
--
ALTER TABLE `producttype`
  MODIFY `type_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `salestransaction`
--
ALTER TABLE `salestransaction`
  MODIFY `transaction_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `shoppingbasket`
--
ALTER TABLE `shoppingbasket`
  MODIFY `basket_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `shoppingcartitem`
--
ALTER TABLE `shoppingcartitem`
  MODIFY `cart_item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `specialoffer`
--
ALTER TABLE `specialoffer`
  MODIFY `offer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `creditcard`
--
ALTER TABLE `creditcard`
  ADD CONSTRAINT `creditcard_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE CASCADE;

--
-- Constraints for table `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `product_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `producttype` (`type_id`);

--
-- Constraints for table `salestransaction`
--
ALTER TABLE `salestransaction`
  ADD CONSTRAINT `salestransaction_ibfk_1` FOREIGN KEY (`basket_id`) REFERENCES `shoppingbasket` (`basket_id`),
  ADD CONSTRAINT `salestransaction_ibfk_2` FOREIGN KEY (`card_number`) REFERENCES `creditcard` (`card_number`),
  ADD CONSTRAINT `salestransaction_ibfk_3` FOREIGN KEY (`shipping_customer_id`,`shipping_address_name`) REFERENCES `shippingaddress` (`customer_id`, `address_name`);

--
-- Constraints for table `shippingaddress`
--
ALTER TABLE `shippingaddress`
  ADD CONSTRAINT `shippingaddress_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`) ON DELETE CASCADE;

--
-- Constraints for table `shoppingbasket`
--
ALTER TABLE `shoppingbasket`
  ADD CONSTRAINT `shoppingbasket_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`customer_id`);

--
-- Constraints for table `shoppingcartitem`
--
ALTER TABLE `shoppingcartitem`
  ADD CONSTRAINT `shoppingcartitem_ibfk_1` FOREIGN KEY (`basket_id`) REFERENCES `shoppingbasket` (`basket_id`),
  ADD CONSTRAINT `shoppingcartitem_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`);

--
-- Constraints for table `specialoffer`
--
ALTER TABLE `specialoffer`
  ADD CONSTRAINT `specialoffer_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`);

--
-- Constraints for table `transactiondetails`
--
ALTER TABLE `transactiondetails`
  ADD CONSTRAINT `transactiondetails_ibfk_1` FOREIGN KEY (`transaction_id`) REFERENCES `salestransaction` (`transaction_id`),
  ADD CONSTRAINT `transactiondetails_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
