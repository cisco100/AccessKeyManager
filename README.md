# Access Key Manager

## Project Overview

The Access Key Manager is a web application developed for Micro-Focus Inc. to manage access keys for their multi-tenant school management platform. This application allows schools to purchase and manage access keys to activate their accounts on the platform, providing a streamlined monetization approach without integrating payment features directly into the school software.
This project is hosted at PythonAnyWhere. View it [here](http://rawdreamz.pythonanywhere.com).

## Features

### For School IT Personnel

1. **User Authentication**
   - Sign up with email and password
   - Email verification required after signup
   - Secure login system
   - Password reset functionality

2. **Access Key Management**
   - View all assigned access keys (active, expired, or revoked)
   - See key details including status, procurement date, and expiry date
   - Request new access key (only if no active key exists)

3. **Dashboard**
   - Personalized dashboard showing keys associated with the school
   - Clear display of key status, procurement date, and expiry date
   - Option to request a new key when no active key is present

### For Micro-Focus Admins

1. **User Authentication**
   - Secure login with predefined admin credentials

2. **Access Key Oversight**
   - View all keys generated on the platform
   - See key details including status, procurement date, and expiry date
   - Ability to manually revoke keys

3. **Dashboard**
   - Comprehensive table of all schools and their respective keys
   - Key management actions (e.g., revocation)

4. **API Endpoint**
   - Special endpoint to check active keys for a given school email
   - Returns key details if an active key is found (status code 200)
   - Returns 404 if no active key is found

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/your-username/access-key-manager.git
   ```

2. Install dependencies:
   ```
   cd AccessKeyManager 
    
   ```

3. Set up the database:
   ```
   
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create a superuser (Micro-Focus Admin):
   ```
   python manage.py createsuperuser
   ```
   Use email: admin@admin.com and set a secure password when prompted.

5. Start the development server:
   ```
   python manage.py runserver
   ```

## Usage Guide

### For School IT Personnel

1. Navigate to the application URL and click on "Sign Up".
2. Fill in your details and submit the registration form.
3. Check your email for a 6-digit verification code.
4. Enter the verification code on the verification page.
5. Once verified, log in with your credentials.
6. You will be directed to your dashboard showing your school's access keys.
7. If no active key is present, use the "Request New Key" button to obtain one.

### For Micro-Focus Admins

1. Navigate to the application URL and click on "Login".
2. Use the admin email (admin@admin.com) and the password set during superuser creation.
3. You will be directed to the admin dashboard showing all schools and their keys.
4. Use the provided interface to manage keys, including revoking them if necessary.

## API Documentation

### Check Active Key Endpoint

- **URL**: `/api/check-active-key/`
- **Method**: GET
- **URL Params**: `email=[string]`
- **Success Response**:
  - Code: 200
  - Content: `{ "key": "key_details_here" }`
- **Error Response**:
  - Code: 404
  - Content: `{ "message": "No active key found" }`

 
