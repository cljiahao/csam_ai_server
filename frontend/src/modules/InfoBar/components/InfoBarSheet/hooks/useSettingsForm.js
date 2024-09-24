import { useFetch } from "@/hooks/useFetch";

const useSettingsForm = () => {
  const { data, error, fetchData } = useFetch();
  return <div>useSettingsForm</div>;
};

export default useSettingsForm;
