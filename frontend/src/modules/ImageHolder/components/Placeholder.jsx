const Placeholder = ({ children }) => {
  return (
    <div className="flex-center m-auto mx-10 h-5/6 w-full rounded-xl border-4 border-dashed border-gray-400 bg-gray-100">
      <p className="flex-center hw-full text-bold text-3xl text-red-500">
        {children}
      </p>
    </div>
  );
};

export default Placeholder;
