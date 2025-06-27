import { z } from "zod";

const colorSchema = z.object({
  defect_label: z.string().min(1, "Label cannot be empty"),
  hex_color: z.string().regex(/^#[0-9a-fA-F]{6}$/, "Invalid color format"),
});

const useColorValidation = () => {
  const validateAdd = (colors, newColor) => {
    const validationResult = colorSchema.safeParse(newColor);
    if (!validationResult.success) {
      return validationResult.error.errors[0].message;
    }
    const labelExists = colors.some(
      (entry) =>
        entry.defect_label.toLowerCase() ===
        newColor.defect_label.toLowerCase(),
    );
    if (labelExists) {
      return "Label exists";
    }
    const colorExists = colors.some(
      (entry) =>
        entry.hex_color.toLowerCase() === newColor.hex_color.toLowerCase(),
    );
    if (colorExists) {
      return "Color  exists";
    }
    return null;
  };

  const validateLabelChange = (colors, index, newLabel) => {
    const trimmedLabel = newLabel.trim();
    if (!trimmedLabel) {
      return "Label empty";
    }
    const lowerNewLabel = trimmedLabel.toLowerCase();
    const labelExists = colors.some(
      (entry, i) =>
        i !== index &&
        entry.defect_label.trim().toLowerCase() === lowerNewLabel,
    );
    if (labelExists) {
      return "Label exists";
    }
    return null;
  };

  const validateColorChange = (colors, index, newColor) => {
    const colorExists = colors.some(
      (entry, i) =>
        i !== index && entry.hex_color.toLowerCase() === newColor.toLowerCase(),
    );
    if (colorExists) {
      return "Color exists";
    }
    return null;
  };

  return { validateAdd, validateLabelChange, validateColorChange };
};

export default useColorValidation;
