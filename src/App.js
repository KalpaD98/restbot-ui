import './App.css';
import ChatWidget from './components/Widget'

function App() {
    localStorage.clear()
    return (<div className="App">
        <ChatWidget/>
    </div>);
}

export default App;