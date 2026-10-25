import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@fontsource/cairo/400.css';
import '@fontsource/cairo/600.css';
import '@fontsource/cairo/800.css';
import '@fontsource/almarai/700.css';
import '@fontsource/almarai/800.css';
import './styles.css';
import App from './App';
import { ErrorBoundary } from './ErrorBoundary';
import { startAnalytics } from './lib/analytics';
import { initInstall } from './lib/install';

startAnalytics();
initInstall();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
);
