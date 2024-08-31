import { useEffect, useState } from "react";
import { getAllFolColor, setAllFolColor } from "@/services/api_defects";
import { useFetch } from "./useFetch";
import { useCallback } from "react";

export function useFolderHex() {
  const { data, error, isLoading, fetchData } = useFetch();
  const [folderHex, setFolderHex] = useState([]);

  // No dependencies, runs once on mount
  useEffect(() => {
    refreshFolderHex();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Update FolderHex state when fetchData changes
  useEffect(() => {
    if (data) setFolderHex(data.colorGroup);
  }, [data]);

  // Fetches folder color data from the API.
  const refreshFolderHex = useCallback(() => {
    fetchData(getAllFolColor, true);
  }, [fetchData]);

  // Amends a specific item in the folderHex state.
  const amendFolderHex = useCallback((item_type, amend_data) => {
    setFolderHex((prevFolderHex) =>
      prevFolderHex.map((obj) =>
        obj.item === item_type ? { ...obj, colors: amend_data } : obj,
      ),
    );
  }, []);

  // Updates the folder color data in the API with the current state.
  const updateFolderHex = useCallback(() => {
    fetchData(() => setAllFolColor({ colorGroup: folderHex }));
  }, [fetchData, folderHex]);

  return {
    error,
    isLoading,
    folderHex,
    refreshFolderHex,
    amendFolderHex,
    updateFolderHex,
  };
}
