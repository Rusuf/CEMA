import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import Table from '../components/common/Table';
import Input from '../components/common/Input';
import PageHeader from '../components/common/PageHeader';
import FormContainer from '../components/common/FormContainer';
import useFetch from '../hooks/useFetch';
import { clientsApi, programsApi, enrollmentsApi } from '../services/api';

const ClientDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data: client, loading, execute: fetchClient } = useFetch(null);
  const { data: programs = [], execute: fetchPrograms } = useFetch([]);
  const [showEnrollForm, setShowEnrollForm] = useState(false);
  const [selectedProgram, setSelectedProgram] = useState('');
  const [enrollmentDate, setEnrollmentDate] = useState(new Date().toISOString().split('T')[0]);

  const enrollmentColumns = [
    { header: 'Program ID', accessor: 'program_id' },
    { header: 'Program Name', accessor: 'program_name' },
    { 
      header: 'Enrollment Date', 
      accessor: 'enrollment_date',
      cell: (row) => new Date(row.enrollment_date).toLocaleDateString()
    }
  ];

  const fetchClientData = async () => {
    await fetchClient(clientsApi.getById, id);
  };

  useEffect(() => {
    const loadData = async () => {
      await fetchClientData();
      await fetchPrograms(programsApi.getAll);
    };
    loadData();
  }, [id]);

  const handleEnroll = async (e) => {
    e.preventDefault();
    if (!selectedProgram) return;

    try {
      await enrollmentsApi.createEnrollment(id, {
        program_id: parseInt(selectedProgram),
        enrollment_date: enrollmentDate
      });
      
      // Reset form
      setSelectedProgram('');
      setEnrollmentDate(new Date().toISOString().split('T')[0]);
      setShowEnrollForm(false);
      
      // Refresh client data to show the new enrollment
      fetchClientData();
    } catch (error) {
      console.error('Error enrolling client:', error);
    }
  };

  const handleToggleEnrollForm = () => {
    setShowEnrollForm(!showEnrollForm);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <p>Loading client details...</p>
      </div>
    );
  }

  if (!client) {
    return (
      <div className="text-center py-8">
        <p className="text-lg text-red-600">Client not found</p>
        <Button className="mt-4" onClick={() => navigate('/clients')}>
          Back to Clients
        </Button>
      </div>
    );
  }

  return (
    <div>
      <PageHeader 
        title="Client Details"
        subtitle={`Viewing profile for ${client.name}`}
        showAction={true}
        actionText="Back to Clients"
        actionVariant="outline"
        onActionClick={() => navigate('/clients')}
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card className="md:col-span-2">
          <div className="space-y-4">
            <div>
              <h3 className="text-sm font-medium text-gray-500">Name</h3>
              <p className="mt-1 text-lg text-gray-900">{client.name}</p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500">Date of Birth</h3>
              <p className="mt-1 text-lg text-gray-900">
                {new Date(client.date_of_birth).toLocaleDateString()}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500">Gender</h3>
              <p className="mt-1 text-lg text-gray-900">
                {client.gender 
                  ? client.gender.charAt(0).toUpperCase() + client.gender.slice(1) 
                  : 'Not specified'}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500">Contact Information</h3>
              <p className="mt-1 text-lg text-gray-900">
                {client.contact_info || 'Not provided'}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500">Client ID</h3>
              <p className="mt-1 text-lg text-gray-900">{client.id}</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-medium text-gray-900">Actions</h3>
          </div>
          <div className="space-y-2">
            <Button
              className="w-full"
              onClick={handleToggleEnrollForm}
            >
              {showEnrollForm ? 'Cancel' : 'Enroll in Program'}
            </Button>
          </div>
        </Card>
      </div>

      {showEnrollForm && (
        <FormContainer 
          title="Enroll in Health Program" 
          onSubmit={handleEnroll}
          onCancel={handleToggleEnrollForm}
          submitText="Enroll Client"
        >
          <div className="mb-4">
            <label htmlFor="program" className="block text-sm font-medium text-gray-700 mb-1">
              Select Program <span className="text-red-500">*</span>
            </label>
            <select
              id="program"
              value={selectedProgram}
              onChange={(e) => setSelectedProgram(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              required
            >
              <option value="">Select a program</option>
              {programs.map((program) => (
                <option key={program.id} value={program.id}>
                  {program.name}
                </option>
              ))}
            </select>
          </div>
          <Input
            label="Enrollment Date"
            id="enrollmentDate"
            name="enrollmentDate"
            type="date"
            value={enrollmentDate}
            onChange={(e) => setEnrollmentDate(e.target.value)}
            required
          />
        </FormContainer>
      )}

      <Card title="Program Enrollments">
        {client.enrollments && client.enrollments.length > 0 ? (
          <Table columns={enrollmentColumns} data={client.enrollments} />
        ) : (
          <p className="text-center py-4 text-gray-500">
            Client is not enrolled in any programs
          </p>
        )}
      </Card>
    </div>
  );
};

export default ClientDetail; 