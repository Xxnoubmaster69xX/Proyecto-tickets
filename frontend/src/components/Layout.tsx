import type { ReactNode } from 'react';
import { Sidebar } from './Sidebar';
import { DynamicBackground } from './DynamicBackground';

interface LayoutProps {
  children: ReactNode;
  isLoggedIn: boolean;
  onLogout: () => void;
}

export const Layout = ({ children, isLoggedIn, onLogout }: LayoutProps) => {
  return (
    <div className="flex min-h-screen bg-transparent relative overflow-hidden">
      <DynamicBackground />
      <Sidebar isLoggedIn={isLoggedIn} onLogout={onLogout} />
      <main className="flex-1 overflow-x-hidden overflow-y-auto z-10">
        <div className="p-8 max-w-7xl mx-auto">
          {children}
        </div>
      </main>
    </div>
  );
};
