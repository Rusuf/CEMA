import React from 'react';
import Card from './Card';
import Input from './Input';
import Button from './Button';

/**
 * Reusable search bar component
 * @param {Object} props - Component props
 * @param {String} props.value - Current search term value
 * @param {Function} props.onChange - Handler for search input change
 * @param {Function} props.onSearch - Handler for search form submission
 * @param {String} props.placeholder - Placeholder text for search input
 * @param {String} props.buttonText - Text for search button
 * @param {String} props.className - Additional class names
 */
const SearchBar = ({
  value = '',
  onChange,
  onSearch,
  placeholder = 'Search...',
  buttonText = 'Search',
  className = ''
}) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(value);
  };

  return (
    <Card className={`mb-6 ${className}`}>
      <form onSubmit={handleSubmit} className="flex space-x-4">
        <Input
          id="search"
          name="search"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="mb-0 flex-1"
        />
        <Button type="submit">{buttonText}</Button>
      </form>
    </Card>
  );
};

export default SearchBar; 