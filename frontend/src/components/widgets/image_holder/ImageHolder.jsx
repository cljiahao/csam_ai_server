import PanAndZoom from "./components/PanAndZoom";
import Placeholder from "./components/PlaceHolder";

const ImageHolder = ({ children, image, placeholder_text }) => {
  return (
    <div className="hw-full flex-center">
      {image ? (
        <PanAndZoom image={image}>{children}</PanAndZoom>
      ) : (
        <Placeholder text={placeholder_text} />
      )}
    </div>
  );
};

export default ImageHolder;
