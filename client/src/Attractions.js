import { useEffect, useState, useRef, useMemo } from "react";

// Component for attraction details panel
export function AttractionDetails({
  attraction,
  onHide,
  onTellMore,
}) {
  return attraction && (
    <div className="m-2 p-2 overflow-y-auto">
      <div><img src={attraction.image} /></div>
      <div className="text-lg font-bold">{attraction.name}</div>
      <div>{attraction.description}</div>
      <div>{attraction.category}</div>
      <div>{attraction.rating}</div>
      <div>Hours: {attraction.hours}</div>
      <div>{attraction.duration}</div>
      <div>Address: {attraction.address}</div>
      <div className="flex flex-row gap-2 mt-2">
        <a
          className="border rounded-full px-4 py-2 inline-block cursor-pointer hover:bg-slate-100"
          onClick={() => onTellMore(attraction.name)}
        >Tell me more</a>
        <a
          className="border rounded-full px-4 py-2 inline-block cursor-pointer hover:bg-slate-100"
          onClick={onHide}
        >Done</a>
      </div>
    </div>
  );
}

// Component for attraction item in the attractions list
export function Attraction({
  id,
  showAttraction,
}) {
  const [attraction, setAttraction] = useState(null);

  useEffect(() => {
    // Get details about the attraction given its attraction id
    fetch("http://localhost:8000/api/attraction", {
      method: "POST",
      body: JSON.stringify({
        id
      })
    }).then((response) => {
      response.json().then((data) => {
        setAttraction(data);
      });
    });
  }, [id]);

  return attraction && attraction.id && (
    <div
      className="m-2 p-2 cursor-pointer hover:bg-slate-100"
      onClick={() => showAttraction(attraction)}
    >
      <div><img src={attraction.image} /></div>
      <div className="text-sm text-center">{attraction.name}</div>
    </div>
  );
}

// Component for list of attractions
export function Attractions({
  attractions,
  showAttraction,
}) {
  const renderedAttractions = useMemo(() =>
    attractions.map((attraction) => (
      <Attraction
        key={attraction.id}
        id={attraction.id}
        showAttraction={showAttraction}
      />
    ))
  , [attractions]);

  return renderedAttractions;
}
