import { useCallback, useEffect, useState } from "react";

export function useFetch() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const fetchData = useCallback(async (req, use_state = false) => {
    if (typeof req !== "function") return;
    setIsLoading(true);
    try {
      const response = await req();
      const result = await response.json();
      if (!response.ok)
        throw result || { details: "An error occurred while fetching data." };
      setError(null);
      if (use_state) setData(result);
    } catch (error) {
      console.log(JSON.stringify(error));
      setError(error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData(); // Fetch data on initial mount
  }, [fetchData]);

  return { data, error, isLoading, fetchData };
}
