import { useState, useCallback } from 'react';
import { handleError } from '../utils/errorHandler';

/**
 * Custom hook to handle API requests with loading state and error handling
 * @param {Function} apiCallFn - API call function to execute
 * @param {*} initialData - Initial state for the data
 */
const useFetch = (initialData = null) => {
  const [data, setData] = useState(initialData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(async (apiCallFn, ...args) => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiCallFn(...args);
      setData(response.data);
      return response.data;
    } catch (err) {
      const errorMessage = handleError(err, apiCallFn.name || 'useFetch');
      setError(errorMessage);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return { data, loading, error, execute, setData, clearError };
};

export default useFetch; 