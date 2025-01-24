const Error = ({ message }) => {
  return (
    <div className="flex h-screen w-full items-center justify-center bg-red-50 text-xl">
      <div
        className="relative rounded border border-red-200 bg-red-100 px-4 py-3 text-red-800"
        role="alert"
      >
        <strong className="font-bold">Error: </strong>
        <span className="block sm:inline">{message}</span>
      </div>
    </div>
  );
};

export default Error;
