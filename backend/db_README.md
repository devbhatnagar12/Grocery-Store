# Database Documentation

## Overview

The database is designed for a web application using Flask-SQLAlchemy and Flask-Security. It consists of several tables: `roles_users`, `role`, `user`, `section`, `product`, `cart_product`, `shopping_cart`, and `purchase`.

## Tables

### RolesUsers

This is a junction table for many-to-many relationship between `user` and `role` tables.

- `id`: Primary key.
- `user_id`: Foreign key referencing `user.id`.
- `role_id`: Foreign key referencing `role.id`.

### Role

This table stores the roles for users.

- `id`: Primary key.
- `name`: Role name, unique.
- `description`: Role description.

### User

This table stores the user data.

- `id`: Primary key.
- `username`: User's username, unique.
- `email`: User's email, unique.
- `password`: User's password.
- `active`: Boolean flag indicating if the user is active.
- `fs_uniquifier`: Flask-Security uniquifier, unique and not nullable.
- `roles`: Relationship with `Role` model, many-to-many.
- `section`: Relationship with `Section` model, one-to-many.
- `purchases`: Relationship with `Purchase` model, one-to-many.

### Section

This table stores the sections created by users.

- `id`: Primary key.
- `name`: Section name.
- `creator_id`: Foreign key referencing `user.id`.
- `status`: Boolean flag indicating the status of the section.
- `products`: Relationship with `Product` model, one-to-many.

### Product

This table stores the products in each section.

- `id`: Primary key.
- `name`: Product name.
- `description`: Product description.
- `price`: Product price.
- `section_id`: Foreign key referencing `section.id`.
- `unit`: Unit of product.
- `stock`: Stock of product.
- `created_at`: Creation timestamp.
- `expired_at`: Expiration timestamp.

### cart_product

This is a junction table for many-to-many relationship between `shopping_cart` and `product` tables.

- `cart_id`: Foreign key referencing `shopping_cart.id`.
- `product_id`: Foreign key referencing `product.id`.

### ShoppingCart

This table stores the shopping carts for users.

- `id`: Primary key.
- `user_id`: Foreign key referencing `user.id`.
- `product_id`: Foreign key referencing `product.id`.
- `quantity`: Quantity of product.
- `products`: Relationship with `Product` model, many-to-many.

### Purchase

This table stores the purchases made by users.

- `id`: Primary key.
- `order_id`: Order ID, not nullable.
- `user_id`: Foreign key referencing `user.id`.
- `product_id`: Foreign key referencing `product.id`.
- `quantity`: Quantity of product.
- `purchase_date`: Purchase date.
- `product`: Relationship with `Product` model, one-to-many.

## Relationships

- `User` and `Role` have a many-to-many relationship through `RolesUsers`.
- `User` has a one-to-many relationship with `Section`.
- `User` has a one-to-many relationship with `Purchase`.
- `Section` has a one-to-many relationship with `Product`.
- `ShoppingCart` and `Product` have a many-to-many relationship through `cart_product`.
- `Purchase` has a one-to-many relationship with `Product`.