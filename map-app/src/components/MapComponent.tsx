import React, { useEffect, useRef, useState, useCallback } from "react";
import "ol/ol.css";
import { Map, View } from "ol";
import { Tile as TileLayer, Vector as VectorLayer } from "ol/layer";
import { OSM } from "ol/source";
import { Vector as VectorSource } from "ol/source";
import { Geometry, Point } from "ol/geom";
import { Feature } from "ol";
import { FeatureLike } from "ol/Feature";
import { fromLonLat } from "ol/proj";
import { Style, Icon, Text, Fill, Stroke } from "ol/style";
import { fetchPoints, addPoint, deletePoint, fetchUser } from "../services/api";
import Overlay from "ol/Overlay";

const MapComponent: React.FC = () => {
  const mapElement = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<Map | null>(null);
  const vectorSource = useRef(new VectorSource()).current;
  const [user, setUser] = useState<any>(null);
  const [overlay, setOverlay] = useState<Overlay | null>(null);
  const [isAddMode, setIsAddMode] = useState(false);

  useEffect(() => {
    const initializeMap = async () => {
      if (mapElement.current && !mapRef.current) {
        const initialMap = new Map({
          target: mapElement.current!,
          layers: [
            new TileLayer({
              source: new OSM(),
            }),
            new VectorLayer({
              source: vectorSource,
            }),
          ],
          view: new View({
            center: fromLonLat([0, 0]),
            zoom: 2,
          }),
        });

        const container = document.getElementById("popup")!;
        const closer = document.getElementById("popup-closer")!;

        const overlay = new Overlay({
          element: container,
          autoPan: {
            animation: {
              duration: 250,
            },
          },
        });

        initialMap.addOverlay(overlay);
        setOverlay(overlay);

        closer.onclick = function () {
          overlay.setPosition(undefined);
          closer.blur();
          return false;
        };

        mapRef.current = initialMap;

        const points = await fetchPoints();
        points.forEach((point: any) => {
          const feature = new Feature({
            geometry: new Point(fromLonLat([point.longitude, point.latitude])),
            name: point.name,
            description: point.description,
            created_at: point.created_at,
            owner: point.owner,
            id: point.id,
          });

          feature.setStyle(
            new Style({
              image: new Icon({
                src: "https://openlayers.org/en/v4.6.5/examples/data/icon.png",
                scale: 1,
              }),
              text: new Text({
                text: point.name,
                offsetY: 15,
                fill: new Fill({ color: "#000" }),
                stroke: new Stroke({ color: "#fff", width: 2 }),
              }),
            })
          );

          vectorSource.addFeature(feature);
        });

        const currentUser = await fetchUser();
        setUser(currentUser);
      }
    };

    initializeMap();
  }, [vectorSource]);

  const handleMapClick = useCallback(
    (event: any) => {
      if (!mapRef.current || !user || !isAddMode) {
        return;
      }

      const coordinates = mapRef.current.getCoordinateFromPixel(event.pixel);
      if (!coordinates) {
        console.error("Failed to get coordinates from the event");
        return;
      }

      const [longitude, latitude] = fromLonLat(coordinates);

      const name = prompt("Enter name:");
      const description = prompt("Enter description:");

      if (name && description) {
        const newPoint = {
          name,
          description,
          latitude,
          longitude,
        };

        addPoint(newPoint)
          .then((point) => {
            const feature = new Feature({
              geometry: new Point(coordinates),
              name: point.name,
              description: point.description,
              owner: user.username,
              id: point.id,
              created_at: new Date().toISOString(),
            });

            feature.setStyle(
              new Style({
                image: new Icon({
                  src: "https://openlayers.org/en/v4.6.5/examples/data/icon.png",
                  scale: 1,
                }),
                text: new Text({
                  text: point.name,
                  offsetY: 15,
                  fill: new Fill({ color: "#000" }),
                  stroke: new Stroke({ color: "#fff", width: 2 }),
                }),
              })
            );

            vectorSource.addFeature(feature);
          })
          .catch((error) => {
            console.error("Error adding point:", error);
          });
      }
    },
    [isAddMode, user, vectorSource]
  );

  const handleFeatureClick = useCallback(
    (feature: Feature<Geometry>) => {
      if (!user) return;
      const geometry = feature.getGeometry();
      if (!(geometry instanceof Point)) return;

      const coordinates = (geometry as Point).getCoordinates();
      const content = document.getElementById("popup-content")!;
      const owner = feature.get("owner");
      const description = feature.get("description");
      const createdAt = new Date(feature.get("created_at")).toLocaleString();
      const id = feature.get("id");
      const isOwner = user.username === owner;

      content.innerHTML = `
            <b>${feature.get("name")}</b><br/>
            <i>Owner: ${owner}</i><br/>
            <p>${description}</p>
            <p>Created at: ${createdAt}</p>
            ${isOwner ? `<button id="delete-point">Delete</button>` : ""}
        `;

      if (overlay) {
        overlay.setPosition(coordinates);
      }

      if (isOwner) {
        document.getElementById("delete-point")!.onclick = () => {
          deletePoint(id).then(() => {
            vectorSource.removeFeature(feature);
            if (overlay) {
              overlay.setPosition(undefined);
            }
          });
        };
      }
    },
    [overlay, user, vectorSource]
  );

  useEffect(() => {
    if (mapRef.current) {
      mapRef.current.on("singleclick", handleMapClick);

      mapRef.current.on("click", (event) => {
        mapRef.current?.forEachFeatureAtPixel(
          event.pixel,
          (featureLike: FeatureLike) => {
            if (featureLike instanceof Feature) {
              handleFeatureClick(featureLike as Feature<Geometry>);
            }
          }
        );
      });
    }

    return () => {
      if (mapRef.current) {
        mapRef.current.un("singleclick", handleMapClick);
      }
    };
  }, [handleMapClick, handleFeatureClick]);

  const toggleAddMode = () => {
    setIsAddMode(!isAddMode);
  };

  return (
    <div className="map-container">
      <button className="map-add-button" onClick={toggleAddMode}>
        {isAddMode ? "Exit Add Mode" : "Enter Add Mode"}
      </button>
      <div ref={mapElement} style={{ width: "100%", height: "100%" }} />
      <div id="popup" className="ol-popup">
        <a href="#" id="popup-closer" className="ol-popup-closer"></a>
        <div id="popup-content"></div>
      </div>
    </div>
  );
};

export default MapComponent;
