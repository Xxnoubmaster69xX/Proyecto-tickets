import React, { ReactNode } from 'react';
import { Sidebar } from './Sidebar';

interface LayoutProps {
  children: ReactNode;
  isLoggedIn: boolean;
  onLogout: () => void;
}

export const Layout = ({ children, isLoggedIn, onLogout }: LayoutProps) => {
  return (
    <div className="flex min-h-screen bg-background bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-surfaceLight/30 via-background to-background">
      <Sidebar isLoggedIn={isLoggedIn} onLogout={onLogout} />
      <main className="flex-1 overflow-x-hidden overflow-y-auto">
        <div className="p-8 max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
};
