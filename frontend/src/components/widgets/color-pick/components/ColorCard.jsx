import { FaTrash } from "react-icons/fa";

import { Input } from "@/components/ui/input";
import useColorValidation from "../hooks/useColorValidation";
import { Form } from "@/components/ui/form";
import { useColorPickContext } from "../contexts/useColorPickContext";
import CustomFormField from "../../custom-form-field/CustomFormField";
import ColorInput from "../../color-input/ColorInput";

const ColorCard = ({ id }) => {
  const { labelColors, handleDelete, onChangeColor, onChangeLabel } =
    useColorPickContext();

  const {
    state: { colorFormInfo },
    action: { colorForm },
  } = useColorValidation();

  return (
    <div className="flex-center h-24 w-full gap-3 rounded-xl border-2 border-slate-300 p-3">
      <Form {...colorForm}>
        <form className="hw-full" onSubmit={colorForm.handleSubmit()}>
          {Object.keys(colorFormInfo).map((key) => {
            const { placeholder } = colorFormInfo[key];
            return (
              <CustomFormField
                control={colorForm.control}
                key={key}
                name="defectLabel"
              >
                <div className="hw-full flex-center relative gap-4">
                  <Input
                    id={id}
                    value={labelColors.find((item) => item.uuid === id).label}
                    placeholder={placeholder}
                    onChange={onChangeLabel}
                  />
                  <ColorInput
                    id={id}
                    onChange={onChangeColor}
                    value={labelColors.find((item) => item.uuid === id).color}
                  />
                </div>
              </CustomFormField>
            );
          })}
        </form>
      </Form>
      <div className="h-full opacity-50">
        <FaTrash
          id={id}
          className="h-4 w-4 cursor-pointer"
          onClick={handleDelete}
        />
      </div>
    </div>
  );
};

export default ColorCard;
