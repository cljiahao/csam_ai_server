const API = process.env.REACT_APP_API;

const FOCUS_SCALE = 7;
const mouse_delta = 10;
const marker = {
  color: {
    default: null,
    zoom: "chartreuse",
  },
  radius: { default: 3, zoom: 10, highlight: 1 },
  border: { default: null, highlight: "2px solid red" },
};

const initialArray = {
  chips: null,
  real_ng: {},
};

const initialData = {
  lot_no: null,
  directory: null,
  plate_no: null,
  chip_type: null,
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

const initialFocus = {
  img_shape: { width: 0, height: 0 },
  state: false,
  x: 0,
  y: 0,
  scale: 1,
};

const initialInfo = {
  no_of_chips: 0,
  no_of_batches: 0,
  no_of_pred_ng: 0,
  no_of_real_ng: {},
};

const initialSettings = {
  chip_type: null,
  file_name: null,
  batchUrl: null,
  chipUrl: null,
};

const initialState = {
  error: false,
  image: { src: null, alt: null },
  menu: false,
  folders: {},
};

export {
  API,
  FOCUS_SCALE,
  marker,
  mouse_delta,
  initialArray,
  initialDisplay,
  initialData,
  initialFocus,
  initialInfo,
  initialState,
  initialSettings,
};
