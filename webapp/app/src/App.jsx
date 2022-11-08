import './App.css';
import { Header } from './Header';
import { Content } from './Content';
import { Footer } from './Footer';

function App() {
  return (
    <div className="App">
      <Header title='Англійсько-український онлайн перекладач'/>
      <Content />
      <Footer />
    </div>
  );
}

export default App;
