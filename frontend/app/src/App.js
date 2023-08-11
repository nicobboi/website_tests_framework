import CustomRouter from './router'
import Layout from './components/layout/Layout';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

function App() {
  return (
    <div className="App">
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <Layout>
          {/* ROUTER */}
          <CustomRouter />
        </Layout>
      </LocalizationProvider>
    </div>
  );
}

export default App;
