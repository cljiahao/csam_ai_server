const API = process.env.REACT_APP_API;

const marker = {
  color: {
    _default: "transparent",
    _zoom: "chartreuse",
  },
  radius: { _default: 5, _zoom: 10, _highlight: 1 },
  border: { _default: null, _highlight: "2px solid red" },
};

const initialArray = {
  chips: null,
  folders: {},
  selected: {},
};

const initialDetails = {
  lot: null,
  plate: null,
  item: null,
  directory: null,
  chips: 0,
  batches: 0,
  pred_ng: 0,
  real_ng: {},
};

const initialDisplay = {
  oldX: 0,
  oldY: 0,
  x: 0,
  y: 0,
  scale: 1,
  width: 0,
  height: 0,
};

// uploaded image width and height
const initialFocus = {
  state: false,
  x: 0,
  y: 0,
  scale: 1,
  width: 0,
  height: 0,
};

const initialTrigger = {
  menu: false,
  image: null,
};

export {
  API,
  marker,
  initialArray,
  initialDetails,
  initialDisplay,
  initialFocus,
  initialTrigger,
};
