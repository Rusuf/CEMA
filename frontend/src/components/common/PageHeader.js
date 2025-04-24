import React from 'react';
import Button from './Button';

/**
 * Reusable page header component with title, subtitle, and action button
 * @param {Object} props - Component props
 * @param {String} props.title - Page title
 * @param {String} props.subtitle - Page subtitle
 * @param {Boolean} props.showAction - Whether to show the action button
 * @param {String} props.actionText - Text for the action button
 * @param {Function} props.onActionClick - Action button click handler
 * @param {String} props.actionVariant - Button variant (default, outline, etc.)
 * @param {String} props.className - Additional class names
 */
const PageHeader = ({
  title,
  subtitle,
  showAction = false,
  actionText = '',
  onActionClick,
  actionVariant = 'default',
  className = ''
}) => {
  return (
    <div className={`flex justify-between items-center mb-6 ${className}`}>
      <div>
        <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
        {subtitle && <p className="text-gray-600">{subtitle}</p>}
      </div>
      {showAction && (
        <Button variant={actionVariant} onClick={onActionClick}>
          {actionText}
        </Button>
      )}
    </div>
  );
};

export default PageHeader; 