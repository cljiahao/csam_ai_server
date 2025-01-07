import { z } from "zod";
import { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

import { useFetch } from "@/hooks/useFetch";
import { getItemType } from "@/services/api_retrieve";
import { useInfoBarContext } from "@/modules/InfoBar/contexts/infoBarContext";
import useSaveInput from "../hooks/useSaveInput";

//TODO: Convert ItemType to combobox for typing and selection

const useImageForm = (page) => {
  const saveUserInput = useSaveInput();
  const { data, error, fetchData } = useFetch();
  const { infoDetails, updateInfoDetails } = useInfoBarContext();

  // Sync the image details from the fetch data or handle error
  useEffect(() => {
    saveUserInput(page);
    updateInfoDetails(error ? { item: "" } : data);
  }, [data, error, updateInfoDetails]);

  // Define form fields with their schema, labels, and default values
  const formInfo = {
    lotNo: {
      label: "Lot Number",
      placeholder: "1234567890",
      defaultValues: "",
      schema: z.string().regex(/^[a-zA-Z0-9]{10}$/, {
        message: "Lot Number must be exactly 10 alphanumeric characters.",
      }),
      onBlur: handleItemDisabled,
    },
    item: {
      label: "Item Type",
      placeholder: "GCM32ER71E106KA57",
      defaultValues: "",
      schema: infoDetails.lotNo
        ? z.string().min(1, {
            message: "Please key in Item Type.",
          })
        : z.string().optional(),
      value: infoDetails.item || "",
    },
  };

  // Create the Zod schema for the form validation
  const FormSchema = z.object(
    Object.fromEntries(
      Object.entries(formInfo).map(([key, { schema }]) => [key, schema]),
    ),
  );

  // Initialize the form with react-hook-form and Zod schema resolver
  const form = useForm({
    resolver: zodResolver(FormSchema),
    defaultValues: Object.fromEntries(
      Object.entries(formInfo).map(([key, { defaultValues }]) => [
        key,
        defaultValues,
      ]),
    ),
  });

  // Update form value when infoDetails changes
  // Must place below form to work
  useEffect(() => {
    form.setValue("item", infoDetails.item);
    form.trigger("item");
  }, [infoDetails.item, form]);

  // Handle onBlur event for lot number input
  function handleItemDisabled(e) {
    const value = e.currentTarget.value;
    if (/^[a-zA-Z0-9]{10}$/.test(value)) {
      fetchData(() => getItemType(value), true);
    }
  }

  return [formInfo, form];
};

export default useImageForm;
