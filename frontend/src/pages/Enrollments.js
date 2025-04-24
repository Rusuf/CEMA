import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import Table from '../components/common/Table';
import Button from '../components/common/Button';
import Input from '../components/common/Input';
import { clientsApi, programsApi } from '../services/api';

const Enrollments = () => {
  const navigate = useNavigate();
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchClients();
  }, []);

  const fetchClients = async (search = '') => {
    try {
      setLoading(true);
      const response = await clientsApi.getAll(search);
      setClients(response.data);
    } catch (error) {
      console.error('Error fetching clients:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchClients(searchTerm);
  };

  const handleViewClient = (client) => {
    navigate(`/clients/${client.id}`);
  };

  // Create a processed list of clients with programs they're enrolled in
  const processedClients = clients.map(client => {
    const programNames = client.enrollments && client.enrollments.length > 0
      ? client.enrollments.map(e => e.program && e.program.name).filter(name => name).join(', ')
      : 'None';
    
    return {
      ...client,
      programNames,
      enrollmentCount: client.enrollments ? client.enrollments.length : 0
    };
  });

  const columns = [
    { header: 'Client ID', accessor: 'id' },
    { header: 'Name', accessor: 'name' },
    { header: 'Enrolled Programs', accessor: 'programNames' },
    { header: 'Enrollment Count', accessor: 'enrollmentCount' },
    { 
      header: 'Action',
      cell: (row) => (
        <Button 
          size="sm" 
          onClick={(e) => {
            e.stopPropagation();
            navigate(`/clients/${row.id}`);
          }}
        >
          View Details
        </Button>
      )
    }
  ];

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Program Enrollments</h1>
        <p className="text-gray-600">View and manage client enrollments in health programs</p>
      </div>

      <Card className="mb-6">
        <form onSubmit={handleSearch} className="flex space-x-4">
          <Input
            id="search"
            name="search"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by client name"
            className="mb-0 flex-1"
          />
          <Button type="submit">Search</Button>
        </form>
      </Card>

      <Card title="Client Enrollments">
        {loading ? (
          <p className="text-center py-4">Loading enrollments...</p>
        ) : (
          <Table 
            columns={columns} 
            data={processedClients}
            onRowClick={handleViewClient}
          />
        )}
      </Card>
    </div>
  );
};

export default Enrollments; 