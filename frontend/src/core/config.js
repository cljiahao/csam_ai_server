import { env } from "../env";

const API_URL = env.VITE_API_URL || "http://localhost:8000/api/v1";

const MARKERS = {
  marks: [
    { id: 0, name: "default", color: "transparent", radius: 3 },
    { id: 1, name: "NG", color: "#ffff00", radius: 1 },
    { id: 2, name: "Others", color: "#00ffff", radius: 1 },
  ],
  zoom: { id: 0, name: "zoom", color: "chartreuse", radius: 10 },
};

const ZOOM_SCALE = { scroll: 10, focus: 7 };

export { API_URL, MARKERS, ZOOM_SCALE };
