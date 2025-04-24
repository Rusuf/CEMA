/**
 * Central error handling utility
 */

/**
 * Formats an error message from an API error response
 * @param {Error} error - The error object from the API call
 * @returns {String} Formatted error message
 */
export const formatErrorMessage = (error) => {
  if (!error) return 'An unknown error occurred';
  
  // Handle axios error response
  if (error.response) {
    const { status, data } = error.response;
    
    // Format based on status code
    if (status === 404) {
      return 'The requested resource was not found';
    } else if (status === 400) {
      return data.error || 'The request was invalid';
    } else if (status === 401) {
      return 'Authentication required';
    } else if (status === 403) {
      return 'You do not have permission to access this resource';
    } else if (status === 500) {
      return 'A server error occurred. Please try again later.';
    }
    
    // Return the error message from the response if available
    return data.error || data.message || `Error ${status}: ${data}`;
  }
  
  // Handle network errors
  if (error.request) {
    return 'Network error: Unable to connect to the server';
  }
  
  // Handle other errors
  return error.message || 'An unexpected error occurred';
};

/**
 * Logs an error with contextual information
 * @param {Error} error - The error object
 * @param {String} context - Context where the error occurred
 */
export const logError = (error, context = '') => {
  const timestamp = new Date().toISOString();
  const contextInfo = context ? ` [${context}]` : '';
  
  console.error(`${timestamp}${contextInfo} Error:`, error);
  
  // You could extend this to log to a monitoring service
};

/**
 * Default error handler that can be used across the application
 * @param {Error} error - The error object
 * @param {String} context - Context where the error occurred
 * @returns {String} Formatted error message
 */
export const handleError = (error, context = '') => {
  logError(error, context);
  return formatErrorMessage(error);
};

export default {
  formatErrorMessage,
  logError,
  handleError
}; 