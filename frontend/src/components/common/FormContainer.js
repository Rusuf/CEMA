import React from 'react';
import Card from './Card';
import Button from './Button';

/**
 * Reusable form container component
 * @param {Object} props - Component props
 * @param {String} props.title - Form title
 * @param {Function} props.onSubmit - Form submission handler
 * @param {Function} props.onCancel - Cancel button handler
 * @param {Boolean} props.loading - Loading state
 * @param {String} props.submitText - Text for submit button
 * @param {String} props.cancelText - Text for cancel button
 * @param {String} props.className - Additional class names
 * @param {Boolean} props.showCancel - Whether to show the cancel button
 * @param {React.ReactNode} props.children - Form inputs
 */
const FormContainer = ({
  title,
  onSubmit,
  onCancel,
  loading = false,
  submitText = 'Save',
  cancelText = 'Cancel',
  className = '',
  showCancel = true,
  children
}) => {
  return (
    <Card title={title} className={`mb-6 ${className}`}>
      <form onSubmit={onSubmit}>
        {children}
        <div className="flex justify-end space-x-2 mt-4">
          {showCancel && (
            <Button
              type="button"
              variant="outline"
              onClick={onCancel}
              disabled={loading}
            >
              {cancelText}
            </Button>
          )}
          <Button type="submit" disabled={loading}>
            {loading ? 'Please wait...' : submitText}
          </Button>
        </div>
      </form>
    </Card>
  );
};

export default FormContainer; 