import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";

const MAX_FILE_SIZE = 50000000;
const ACCEPTED_FILE_TYPES = [
  "application/json",
  "application/x-zip-compressed",
];
const useSettingsForm = (page) => {
  // Define form fields with their schema, labels, and default values
  const formInfo = {
    settings: {
      label: `Settings ${page.toUpperCase() === "CDC" ? "" : "and Model File "}Upload`,
      schema: z
        .instanceof(FileList)
        .refine((files) => files?.length !== 0, "File is required")
        .refine(
          (files) => files?.[0]?.size <= MAX_FILE_SIZE,
          `Max image size is 50MB.`,
        )
        .refine(
          (files) => ACCEPTED_FILE_TYPES.includes(files?.[0]?.type),
          "Only .json, .zip formats are supported.",
        ),
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
  });

  return [formInfo, form];
};

export default useSettingsForm;
