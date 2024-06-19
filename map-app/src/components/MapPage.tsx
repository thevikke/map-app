import React from 'react';
import MapComponent from './MapComponent';
import './MapPage.css'; // Ensure this is imported

const MapPage: React.FC = () => {
    return (
        <div className="map-page">
            <MapComponent />
        </div>
    );
};

export default MapPage;

