import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import MapPage from './components/MapPage';
import './App.css';

const App: React.FC = () => {
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/map" element={<MapPage />} />
                    <Route path="/" element={<Navigate to="/login" />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;
