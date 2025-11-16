# SND - Data Specifications

## Authentication Forms

### Login Form
| Name | Type | Constraint | Input Format | Description |
|------|------|------------|--------------|-------------|
| Email | String | Valid email format | Text field | User's email address |
| Password | String | Minimum 6 characters | Password field | User's password |

### Registration Form
| Name | Type | Constraint | Input Format | Description |
|------|------|------------|--------------|-------------|
| FirstName | String | [a-zA-Zа-яА-Я-] {2,50} | Text field | User's first name |
| LastName | String | [a-zA-Zа-яА-Я-] {2,50} | Text field | User's last name |
| Email | String | Valid email format | Text field | User's email address |
| Phone | String | Optional, valid phone format | Text field | User's phone number |
| Password | String | Minimum 6 characters | Password field | User's password |
| ConfirmPassword | String | Must match password | Password field | Password confirmation |

## User Profile Data

### Personal Information
| Name | Type | Constraint | Input Format | Description |
|------|------|------------|--------------|-------------|
| FirstName | String | [a-zA-Zа-яА-Я-] {2,50} | Text field | User's first name |
| LastName | String | [a-zA-Zа-яА-Я-] {2,50} | Text field | User's last name |
| Email | String | Valid email format | Text field | User's email address |
| Phone | String | Optional, valid phone format | Text field | User's phone number |

### Address Information
| Name | Type | Constraint | Input Format | Description |
|------|------|------------|--------------|-------------|
| Country | String | {2, 50} | Text field | Country name |
| Region | String | {0, 50} | Text field | Region/state name |
| City | String | {2, 50} | Text field | City name |
| Street | String | {0, 100} | Text field | Street name |
| House | String | {0, 20} | Text field | House number |
| Apartment | String | {0, 20} | Text field | Apartment number |
| AddressType | String | {1, 10} | Text field | Type of address (e.g., home, work) |

## Product Data

### Product Information
| Name | Type | Constraint | Input Format | Description |
|------|------|------------|--------------|-------------|
| ProductName | String | {1, 200} | Text field | Name of the product |
| Description | Text | {0, 1000} | Text area | Product description |
| Price | Decimal | Positive value | Number field | Product price |
| StockQuantity | Integer | Non-negative | Number field | Available quantity |
| Brand | String | {0, 100} | Text field | Product brand |
| Category | String | {0, 100} | Text field | Product category |

## Cart Data

### Cart Item
| Name | Type | Constraint | Input Format | Description |
|------|------|------------|--------------|-------------|
| ProductID | Integer | Positive | Number field | ID of the product |
| Quantity | Integer | Positive, ≤ stock | Number field | Quantity of product |
| Price | Decimal | Positive | Number field | Price per unit |

## Order Data

### Order Information
| Name | Type | Constraint | Input Format | Description |
|------|------|------------|--------------|-------------|
| CustomerID | Integer | Positive | Number field | ID of the customer |
| TotalAmount | Decimal | Positive | Number field | Total order amount |
| Status | String | {pending, confirmed, shipped, delivered, cancelled} | Select field | Order status |
| ShippingAddress | Text | {10, 500} | Text area | Delivery address |

## Technical Support Request

### Support Ticket
| Name | Type | Constraint | Input Format | Description |
|------|------|------------|--------------|-------------|
| Subject | String | {5, 100} | Text field | Subject of the request |
| Content | String | {20, 1000} | Text area | Detailed description |
| Email | String | Valid email format | Text field | User's email for response |
| Priority | String | {low, medium, high} | Select field | Request priority |