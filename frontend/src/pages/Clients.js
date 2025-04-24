import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import Table from '../components/common/Table';
import Button from '../components/common/Button';
import Input from '../components/common/Input';
import { clientsApi } from '../services/api';

const Clients = () => {
  const navigate = useNavigate();
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    date_of_birth: '',
    contact_info: '',
  });

  const columns = [
    { header: 'ID', accessor: 'id' },
    { header: 'Name', accessor: 'name' },
    { 
      header: 'Date of Birth', 
      accessor: 'date_of_birth',
      cell: (row) => new Date(row.date_of_birth).toLocaleDateString()
    },
    { header: 'Contact Info', accessor: 'contact_info' },
  ];

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

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await clientsApi.create(formData);
      setFormData({ name: '', date_of_birth: '', contact_info: '' });
      setShowForm(false);
      fetchClients();
    } catch (error) {
      console.error('Error creating client:', error);
    }
  };

  const handleViewClient = (client) => {
    navigate(`/clients/${client.id}`);
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Clients</h1>
          <p className="text-gray-600">Manage clients in the system</p>
        </div>
        <Button onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'Register Client'}
        </Button>
      </div>

      {showForm && (
        <Card title="Register New Client" className="mb-6">
          <form onSubmit={handleSubmit}>
            <Input
              label="Client Name"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder="Enter client name"
              required
            />
            <Input
              label="Date of Birth"
              id="date_of_birth"
              name="date_of_birth"
              type="date"
              value={formData.date_of_birth}
              onChange={handleInputChange}
              required
            />
            <Input
              label="Contact Information"
              id="contact_info"
              name="contact_info"
              value={formData.contact_info}
              onChange={handleInputChange}
              placeholder="Enter contact information"
            />
            <div className="flex justify-end">
              <Button type="submit">Save Client</Button>
            </div>
          </form>
        </Card>
      )}

      <Card className="mb-6">
        <form onSubmit={handleSearch} className="flex space-x-4">
          <Input
            id="search"
            name="search"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by name or contact info"
            className="mb-0 flex-1"
          />
          <Button type="submit">Search</Button>
        </form>
      </Card>

      <Card>
        {loading ? (
          <p className="text-center py-4">Loading clients...</p>
        ) : (
          <Table 
            columns={columns} 
            data={clients}
            onRowClick={handleViewClient}
          />
        )}
      </Card>
    </div>
  );
};

export default Clients; 