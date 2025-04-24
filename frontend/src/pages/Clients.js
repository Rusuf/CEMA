import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import Table from '../components/common/Table';
import Input from '../components/common/Input';
import PageHeader from '../components/common/PageHeader';
import FormContainer from '../components/common/FormContainer';
import SearchBar from '../components/common/SearchBar';
import useFetch from '../hooks/useFetch';
import { clientsApi } from '../services/api';

const Clients = () => {
  const navigate = useNavigate();
  const { data: clients, loading, execute } = useFetch([]);
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
    {
      header: 'Programs Enrolled',
      accessor: 'enrollments',
      cell: (row) => row.enrollments && row.enrollments.length > 0
        ? row.enrollments.map(e => e.program_name).join(', ')
        : 'Not enrolled'
    },
  ];

  useEffect(() => {
    fetchClients();
  }, []);

  const fetchClients = async (search = '') => {
    await execute(clientsApi.getAll, search);
  };

  const handleSearch = (term) => {
    fetchClients(term);
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

  const handleToggleForm = () => {
    setShowForm(!showForm);
  };

  const handleViewClient = (client) => {
    navigate(`/clients/${client.id}`);
  };

  return (
    <div>
      <PageHeader 
        title="Clients"
        subtitle="Manage clients in the system"
        showAction={true}
        actionText={showForm ? 'Cancel' : 'Register Client'}
        onActionClick={handleToggleForm}
      />

      {showForm && (
        <FormContainer 
          title="Register New Client" 
          onSubmit={handleSubmit}
          onCancel={handleToggleForm}
          submitText="Save Client"
        >
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
        </FormContainer>
      )}

      <SearchBar 
        value={searchTerm}
        onChange={setSearchTerm}
        onSearch={handleSearch}
        placeholder="Search by name or contact info"
      />

      <Card>
        {loading ? (
          <p className="text-center py-4">Loading clients...</p>
        ) : (
          <Table 
            columns={columns} 
            data={clients || []}
            onRowClick={handleViewClient}
          />
        )}
      </Card>
    </div>
  );
};

export default Clients; 