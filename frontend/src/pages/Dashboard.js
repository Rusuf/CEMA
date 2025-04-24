import React, { useState, useEffect } from 'react';
import Card from '../components/common/Card';
import { programsApi, clientsApi } from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalPrograms: 0,
    totalClients: 0,
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const programsResponse = await programsApi.getAll();
        const clientsResponse = await clientsApi.getAll();

        setStats({
          totalPrograms: programsResponse.data.length,
          totalClients: clientsResponse.data.length,
        });
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
      }
    };

    fetchStats();
  }, []);

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Welcome to CEMA Basic Health Information System</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <Card>
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-primary-100 text-primary-800">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
            </div>
            <div className="ml-5">
              <p className="text-gray-500">Total Programs</p>
              <p className="text-2xl font-semibold text-gray-800">{stats.totalPrograms}</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center">
            <div className="p-3 rounded-full bg-blue-100 text-blue-800">
              <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
            <div className="ml-5">
              <p className="text-gray-500">Total Clients</p>
              <p className="text-2xl font-semibold text-gray-800">{stats.totalClients}</p>
            </div>
          </div>
        </Card>
      </div>

      <Card title="System Overview">
        <p className="text-gray-600">
          CEMA BHIS is a lightweight health information system that helps healthcare workers to:
        </p>
        <ul className="list-disc list-inside mt-2 space-y-1 text-gray-600">
          <li>Create health programs (TB, Malaria, HIV, etc.)</li>
          <li>Register clients into the system</li>
          <li>Enroll clients in one or more health programs</li>
          <li>Search for clients and view their profiles</li>
        </ul>
      </Card>
    </div>
  );
};

export default Dashboard; 