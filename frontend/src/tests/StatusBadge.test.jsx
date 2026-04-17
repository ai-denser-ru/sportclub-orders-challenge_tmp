import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import StatusBadge from '../components/StatusBadge';

describe('StatusBadge', () => {
  it('renders correctly for PAID status', () => {
    // Arrange
    render(<StatusBadge status="PAID" />);
    
    // Act
    const badgeElement = screen.getByText('Paid');
    
    // Assert
    expect(badgeElement).toBeInTheDocument();
    expect(badgeElement).toHaveClass('bg-emerald-500/15', 'text-emerald-400');
  });

  it('renders correctly for PENDING status', () => {
    render(<StatusBadge status="PENDING" />);
    const badgeElement = screen.getByText('Pending');
    expect(badgeElement).toBeInTheDocument();
    expect(badgeElement).toHaveClass('bg-amber-500/15', 'text-amber-400');
  });
});
