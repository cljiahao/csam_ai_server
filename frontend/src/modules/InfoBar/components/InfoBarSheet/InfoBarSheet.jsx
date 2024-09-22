import NavModalSheet from "@/components/NavModalSheet/NavModalSheet";

const InfoBarSheet = () => {
  return (
    <NavModalSheet
      bool_function={(isOpen) => (isOpen ? true : false)}
    ></NavModalSheet>
  );
};

export default InfoBarSheet;
