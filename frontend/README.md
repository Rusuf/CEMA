# CEMA BHIS Frontend

This directory contains the frontend code for the CEMA Basic Health Information System.

## Features

- User-friendly interface for healthcare workers
- Client registration and search
- Health program management
- Client enrollment in health programs
- Dashboard for viewing client profiles and program enrollments

## Technology Stack

- React.js
- Tailwind CSS for styling
- React Router for navigation
- Axios for API calls

## Getting Started

1. Make sure you have Node.js installed (v14+ recommended)
2. Install dependencies:
   ```
   cd frontend
   npm install
   ```
3. Start the development server:
   ```
   npm start
   ```
4. The frontend will be available at http://localhost:3000

## Backend Connection

The frontend connects to the backend API which should be running at http://localhost:8000.
Make sure the backend server is running before using the frontend.

## Project Structure

- `/src/components`: Reusable UI components
- `/src/pages`: Page components for different routes
- `/src/services`: API service for backend communication 