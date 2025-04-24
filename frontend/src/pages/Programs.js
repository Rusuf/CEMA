import React, { useState, useEffect } from 'react';
import Card from '../components/common/Card';
import Table from '../components/common/Table';
import Input from '../components/common/Input';
import PageHeader from '../components/common/PageHeader';
import FormContainer from '../components/common/FormContainer';
import useFetch from '../hooks/useFetch';
import { programsApi } from '../services/api';

const Programs = () => {
  const { data: programs, loading, execute } = useFetch([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
  });

  const columns = [
    { header: 'ID', accessor: 'id' },
    { header: 'Name', accessor: 'name' },
    { header: 'Description', accessor: 'description' },
  ];

  useEffect(() => {
    fetchPrograms();
  }, []);

  const fetchPrograms = async () => {
    await execute(programsApi.getAll);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await programsApi.create(formData);
      setFormData({ name: '', description: '' });
      setShowForm(false);
      fetchPrograms();
    } catch (error) {
      console.error('Error creating program:', error);
    }
  };

  const handleToggleForm = () => {
    setShowForm(!showForm);
  };

  return (
    <div>
      <PageHeader 
        title="Programs"
        subtitle="Manage health programs in the system"
        showAction={true}
        actionText={showForm ? 'Cancel' : 'Add Program'}
        onActionClick={handleToggleForm}
      />

      {showForm && (
        <FormContainer 
          title="Add New Program" 
          onSubmit={handleSubmit}
          onCancel={handleToggleForm}
          submitText="Save Program"
        >
          <Input
            label="Program Name"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            placeholder="Enter program name"
            required
          />
          <Input
            label="Description"
            id="description"
            name="description"
            value={formData.description}
            onChange={handleInputChange}
            placeholder="Enter program description"
          />
        </FormContainer>
      )}

      <Card>
        {loading ? (
          <p className="text-center py-4">Loading programs...</p>
        ) : (
          <Table columns={columns} data={programs || []} />
        )}
      </Card>
    </div>
  );
};

export default Programs; 