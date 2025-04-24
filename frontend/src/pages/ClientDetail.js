import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import Table from '../components/common/Table';
import Input from '../components/common/Input';
import { clientsApi, programsApi, enrollmentsApi } from '../services/api';

const ClientDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [client, setClient] = useState(null);
  const [programs, setPrograms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showEnrollForm, setShowEnrollForm] = useState(false);
  const [selectedProgram, setSelectedProgram] = useState('');
  const [enrollmentDate, setEnrollmentDate] = useState(new Date().toISOString().split('T')[0]);

  const enrollmentColumns = [
    { header: 'Program ID', accessor: 'program_id' },
    { header: 'Program Name', accessor: 'program.name' },
    { 
      header: 'Enrollment Date', 
      accessor: 'enrollment_date',
      cell: (row) => new Date(row.enrollment_date).toLocaleDateString()
    }
  ];

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const clientResponse = await clientsApi.getById(id);
        setClient(clientResponse.data);
        
        const programsResponse = await programsApi.getAll();
        setPrograms(programsResponse.data);
      } catch (error) {
        console.error('Error fetching client details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const handleEnroll = async (e) => {
    e.preventDefault();
    if (!selectedProgram) return;

    try {
      await enrollmentsApi.createEnrollment(id, {
        program_id: parseInt(selectedProgram),
        enrollment_date: enrollmentDate
      });
      
      // Refresh client data to show the new enrollment
      const clientResponse = await clientsApi.getById(id);
      setClient(clientResponse.data);
      
      // Reset form
      setSelectedProgram('');
      setEnrollmentDate(new Date().toISOString().split('T')[0]);
      setShowEnrollForm(false);
    } catch (error) {
      console.error('Error enrolling client:', error);
    }
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
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Client Details</h1>
          <p className="text-gray-600">
            Viewing profile for {client.name}
          </p>
        </div>
        <Button variant="outline" onClick={() => navigate('/clients')}>
          Back to Clients
        </Button>
      </div>

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
              onClick={() => setShowEnrollForm(!showEnrollForm)}
            >
              {showEnrollForm ? 'Cancel' : 'Enroll in Program'}
            </Button>
          </div>
        </Card>
      </div>

      {showEnrollForm && (
        <Card title="Enroll in Health Program" className="mb-6">
          <form onSubmit={handleEnroll}>
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
            <div className="flex justify-end">
              <Button type="submit">Enroll Client</Button>
            </div>
          </form>
        </Card>
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