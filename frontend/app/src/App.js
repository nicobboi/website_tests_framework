import CustomRouter from './router'
import Layout from './components/layout/Layout';

function App() {
  return (
    <div className="App">
        <Layout>
          {/* ROUTER */}
          <CustomRouter />
        </Layout>
    </div>
  );
}

export default App;
