import { HelmetProvider } from "react-helmet-async";
import { Toaster } from "../ui/toaster";

const BaseLayout = ({ children }) => {
  return (
    <HelmetProvider>
      <main className="flex h-screen max-h-screen w-screen overflow-hidden">
        {children}
      </main>
      <Toaster />
    </HelmetProvider>
  );
};

export default BaseLayout;
