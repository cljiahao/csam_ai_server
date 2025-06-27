import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

const useColorValidation = () => {
  const colorFormInfo = {
    defectLabel: {
      label: "Defect Label",
      placeholder: "Defect Label",
      schema: z.string().min(1, { message: "Defect Label cannot be empty." }),
    },
  };

  const colorSchema = z.object(
    Object.fromEntries(
      Object.entries(colorFormInfo).map(([key, { schema }]) => [key, schema]),
    ),
  );

  const colorForm = useForm({
    resolver: zodResolver(colorSchema),
    mode: "onBlur",
    defaultValues: Object.keys(colorFormInfo).reduce((acc, key) => {
      acc[key] = "";
      return acc;
    }, {}),
  });

  return {
    state: { colorFormInfo },
    action: { colorForm },
  };
};

export default useColorValidation;
