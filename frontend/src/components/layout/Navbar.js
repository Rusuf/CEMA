import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <header className="bg-white shadow-sm">
      <div className="px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <h1 className="text-2xl font-bold text-primary-700">CEMA BHIS</h1>
        </div>
        <div className="flex items-center space-x-4">
          <span className="text-sm text-gray-600">Healthcare Management System</span>
        </div>
      </div>
    </header>
  );
};

export default Navbar; 